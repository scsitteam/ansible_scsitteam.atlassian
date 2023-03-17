# -*- coding: utf-8 -*-

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.urls import Request
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.six.moves.urllib.error import HTTPError

import json
from functools import cached_property


class AtlassianApi(object):
    def __init__(self, module):
        self.module = module

    def url(self, url):
        pass

    def get(self, url):
        url = self.url(url)
        try:
            return json.loads(self._cli.get(url).read())
        except HTTPError as e:
            if e.code == 404:
                return None
            data = e.read()
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass
            self.module.fail_json(f"Could not get {url} [{e.code}]: {data}")
        except json.JSONDecodeError as e:
            self.module.fail_json(f"API returned invalid JSON when trying to get {url}: {str(e)}")
        except Exception as e:
            self.module.fail_json(f"Could not get {url}: {str(e)}")

    def post(self, url, payload):
        url = self.url(url)
        try:
            data = self._cli.post(url, data=json.dumps(payload)).read()
            if data:
                return json.loads(data)
            return None
        except HTTPError as e:
            data = e.read()
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass
            self.module.fail_json(f"Could not post {url}: {data}")
        except json.JSONDecodeError as e:
            self.module.fail_json(f"API returned invalid JSON when trying to post {url}: {str(e)}")
        except Exception as e:
            self.module.fail_json(f"Could not post {url}: {str(e)}")

    @cached_property
    def _cli(self):
        cli = Request(
            timeout=self.module.params.get('connection_timeout'),
            validate_certs=self.module.params.get('validate_certs'),
            http_agent=f"Ansible-{self.module.ansible_version}/{self.module._name}",
            url_username=self.module.params.get('atlassian_username'),
            url_password=self.module.params.get('atlassian_password'),
            force_basic_auth=True,
        )

        cli.headers.update({
            'Content-Type': 'application/json'
        })

        return cli


class ConfluenceApi(AtlassianApi):
    def url(self, url):
        return f"https://{self.module.params.get('atlassian_instance')}.atlassian.net/wiki/{url.lstrip('/')}"


class JiraPlatformApi(AtlassianApi):
    def url(self, url):
        return f"https://{self.module.params.get('atlassian_instance')}.atlassian.net/rest/{url.lstrip('/')}"
