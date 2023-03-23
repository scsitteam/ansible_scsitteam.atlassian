#!/usr/bin/python

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = '''
---
module: confluence_space_permission

short_description: Manage Confluence Space

description:
    - Manage a confluence space

options:
    key:
        description:
            - The Confluence Space key
        type: str
        required: true
    user:
        description:
            - The Name of the user to grant permissions to.
        type: str
        required: false
    group:
        description:
            - The Name of the user to grant permissions to.
        type: str
        required: false
    permission:
        description:
            - Dictionary of permissions to grant or revoke.
        type: dict
        suboptions:
            space:
                description:
                    - List of space permissions to grant or revoke.
                type: list
                elements: str
                choices: [read, delete, export, administer, restrict_content]
            page:
                description:
                    - List of space permissions to grant or revoke.
                type: list
                elements: str
                choices: [create, delete, archive]
            blogpost:
                description:
                    - List of space permissions to grant or revoke.
                type: list
                elements: str
                choices: [create, delete]
            comment:
                description:
                    - List of space permissions to grant or revoke.
                type: list
                elements: str
                choices: [create, delete]
            attachment:
                description:
                    - List of space permissions to grant or revoke.
                type: list
                elements: str
                choices: [create, delete]

    state:
        description:
            - The desired state of the space
        type: str
        required: false
        choices: [ grant, revoke, pure ]
        default: grant

extends_documentation_fragment:
- scsitteam.atlassian.atlassian
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
# Create a space
- name: Create a space
  confluence_space:
    key: ANSIBLE
    name: Ansible Space
    private: true

# Delete a space
- name: Create a space
  confluence_space:
    state: absent
    key: ANSIBLE
'''

RETURN = '''
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import ConfluenceApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        key=dict(type='str', required=True, no_log=False),
        # Single permission
        user=dict(type='str'),
        group=dict(type='str'),
        permission=dict(type='dict', default={}, options=dict(
            space=dict(type='list', default=[], elements='str', choices=['read', 'delete', 'export', 'administer', 'restrict_content']),
            page=dict(type='list', default=[], elements='str', choices=['create', 'delete', 'archive']),
            blogpost=dict(type='list', default=[], elements='str', choices=['create', 'delete']),
            comment=dict(type='list', default=[], elements='str', choices=['create', 'delete']),
            attachment=dict(type='list', default=[], elements='str', choices=['create', 'delete']),
        )),
        state=dict(type='str', default='grant', choices=['grant', 'revoke', 'pure']),
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
    state = module.params['state']

    # Setup API
    api = ConfluenceApi(module)

    # Get current state
    current_permissions = api.get(f"/rest/api/space/{key}", params=dict(expand='permissions'))['permissions']
    for current_permission in current_permissions:
        if 'group' in current_permission['subjects']:
            current_permission['subjects']['group'] = [s['name'] for s in current_permission['subjects']['group']['results']]
        if 'user' in current_permission['subjects']:
            current_permission['subjects']['user'] = [s['displayName'] for s in current_permission['subjects']['user']['results']]

    if user:
        current_permissions = [p for p in current_permissions if user in p['subjects'].get('user', [])]
    if group:
        current_permissions = [p for p in current_permissions if group in p['subjects'].get('group', [])]

    result['current_permissions'] = current_permissions

    # Grant
    if state in ['grant', 'pure']:
        from copy import deepcopy
        missing_permissions = deepcopy(module.params['permission'])
        for permission in current_permissions:
            if permission['operation']['operation'] in missing_permissions.get(permission['operation']['targetType'], []):
                missing_permissions[permission['operation']['targetType']].remove(permission['operation']['operation'])

        for target, permissions in missing_permissions.items():
            for permission in permissions:
                payload = dict(
                    operation=dict(
                        key=permission,
                        target=target,
                    )
                )
                if group:
                    payload['subject'] = dict(
                        type='group',
                        identifier=group,
                    )
                result['changed'] = True
                if not module.check_mode:
                    api.post(f"/rest/api/space/{key}/permission", json=payload)

        result['missing_permissions'] = missing_permissions

    # Pure
    if state == 'pure':
        permissions = module.params['permission'].copy()
        result['additional_permissions'] = []
        for permission in current_permissions:
            if permission['operation']['operation'] not in permissions.get(permission['operation']['targetType'], []):
                result['changed'] = True
                if not module.check_mode:
                    api.delete(f"/rest/api/space/{key}/permission/{permission['id']}")
                result['additional_permissions'].append(permission)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
