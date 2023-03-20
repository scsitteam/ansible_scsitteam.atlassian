# -*- coding: utf-8 -*-

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import traceback

from ansible.module_utils.basic import missing_required_lib

try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
    ANOTHER_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_ANOTHER_LIBRARY = True
    ANOTHER_LIBRARY_IMPORT_ERROR = None

from functools import cached_property


class AtlassianApi(object):
    def __init__(self, module):
        self.module = module

    def url(self, url):
        pass

    def get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _request(self, method, url, **kwargs):
        url = self.url(url)
        try:
            resp = self._cli.request(method, url, **kwargs)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            self.module.fail_json(f"Could not {method.upper()} {url}: {str(e)}")
        except requests.JSONDecodeError as e:
            self.module.fail_json(f"API returned invalid JSON when trying to {method.upper()} {url}: {str(e)}")
        except Exception as e:
            self.module.fail_json(f"Could not {method.upper()} {url}: {str(e)}")

    @cached_property
    def _cli(self):
        cli = requests.Session()
        cli.auth = (
            self.module.params.get('atlassian_username'),
            self.module.params.get('atlassian_password')
        )
        cli.headers.update({
            'User-Agent': f"Ansible-{self.module.ansible_version}/{self.module._name}",
            'Content-Type': 'application/json'
        })
        cli.verify = self.module.params.get('validate_certs')

        return cli


class ConfluenceApi(AtlassianApi):
    def url(self, url):
        return f"https://{self.module.params.get('atlassian_instance')}.atlassian.net/wiki/{url.lstrip('/')}"


class JiraPlatformApi(AtlassianApi):
    def url(self, url):
        return f"https://{self.module.params.get('atlassian_instance')}.atlassian.net/rest/{url.lstrip('/')}"
