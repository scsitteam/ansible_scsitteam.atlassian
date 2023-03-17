# -*- coding: utf-8 -*-

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, env_fallback
from functools import cached_property


class AnsibleAtlassianModule(AnsibleModule):
    def __init__(self, argument_spec, **kwargs):
        argument_spec.update(dict(
            atlassian_instance=dict(
                type='str',
                required=False,
                fallback=(env_fallback, ['ATLASSIAN_INSTANCE'])
            ),
            atlassian_username=dict(
                type='str',
                required=False,
                fallback=(env_fallback, ['ATLASSIAN_USERNAME'])
            ),
            atlassian_password=dict(
                type='str',
                required=False,
                fallback=(env_fallback, ['ATLASSIAN_PASSWORD']),
                no_log=True
            ),
            validate_certs=dict(type='bool', default=True),
            connection_timeout=dict(type='int', default=10),
        ))

        super().__init__(argument_spec, **kwargs)
