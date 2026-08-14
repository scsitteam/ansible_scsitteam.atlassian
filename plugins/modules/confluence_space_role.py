#!/usr/bin/python

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = '''
---
module: confluence_space_role

short_description: Manage Confluence Space

description:
    - Manage a confluence space role

options:
    key:
        description:
            - The Confluence Space key
        type: str
        required: true
    user:
        description:
            - The Name of the user to grant a role to.
        type: str
        required: false
    group:
        description:
            - The Name of the user to grant a role to.
        type: str
        required: false
    role:
        description:
            - The Name of the role to grant.
        type: str
        required: false

extends_documentation_fragment:
- scsitteam.atlassian.atlassian
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import ConfluenceApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        key=dict(type='str', required=True, no_log=False),
        user=dict(type='str'),
        group=dict(type='str'),
        role=dict(type='str'),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = AnsibleAtlassianModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ('user', 'group'),
        ],
        required_one_of=[
            ('user', 'group'),
        ],
    )

    # Parameters
    key = module.params['key']
    user = module.params['user']
    group = module.params['group']
    role_name = module.params['role']

    # Setup API
    api = ConfluenceApi(module)

    # Get space
    space = api.get(f"/api/v2/spaces", params=dict(keys=key))['results'][0]
    if space == None:
        module.fail_json(msg=f"Space '{key}' not found.", **result)
    result['space'] = space

    # Get role
    role = next((
        r
        for r in api.get(f"/api/v2/space-roles")['results']
        if r['name'] == role_name
    ), None)
    if role == None:
        module.fail_json(msg=f"Role '{role_name}' not found.", **result)

    # Get principal
    if group is not None:
        principal = next((
            g
            for g in api.get("/rest/api/group/picker", params=dict(query=group))['results']
            if g['name'] == group
        ), None)

    # Get current role
    current_role = next((
        r
        for r in api.get(f"/api/v2/spaces/{space['id']}/role-assignments")['results']
        if r['principal']['principalId'] == principal['id']
    ), None)
    result['current_role'] = current_role

    if current_role is None or current_role['roleId'] != role['id']:
        payload = [dict(
            principal=dict(
                principalType='GROUP',
                principalId=principal['id'],
            ),
            roleId=role['id']
        )]
        result['changed'] = True
        if not module.check_mode:
            api.post(f"api/v2/spaces/{space['id']}/role-assignments", json=payload)


    module.exit_json(**result)


if __name__ == '__main__':
    main()
