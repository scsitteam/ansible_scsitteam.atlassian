#!/usr/bin/python

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = '''
---
module: jira_group_info

short_description: Query Jira Group Infos

description:
    - Manage a confluence space

options:
    name:
        description:
            - The Name of the Jira group
        required: false
        type: str

extends_documentation_fragment:
- scsitteam.atlassian.atlassian
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
# Create a space
- name: Create a space
  jira_group_info:
    name: ansbile-admins
'''

RETURN = '''
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str'),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = AnsibleAtlassianModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Parameters
    name = module.params['name']

    # Setup API
    api = JiraPlatformApi(module)

    # Get current state
    group = api.get(f"/api/2/group/member?groupname={ name }")

    result['group'] = group
    module.exit_json(**result)


if __name__ == '__main__':
    main()
