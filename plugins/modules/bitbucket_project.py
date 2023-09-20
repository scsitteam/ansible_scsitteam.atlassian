# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: bitbucket_project

short_description: Manage Bitbucket Project

description:
    - Manage a Bitbucket Project

options:
    key:
        description:
            - The Bitbucket project key
        required: true
        type: str
    name:
        description:
            - The Name of the Bitbucket project.
        type: str
    description:
        description:
            - The Description of the Bitbucket project
        type: str
    is_private:
        description:
            - If the project is private or not.
        default: True
        type: bool
    group_permission:
        description:
            - Bitbucker Projects Group permissions
        type: dict
        suboptions:
            set:
                description:
                    - Bitbucker Group permissions to set
                type: list
                elements: dict
                suboptions:
                    group:
                        description:
                            - The Name of the group to give permissions to
                        required: true
                        type: str
                    permission:
                        description: Permission to grant
                        choices: ['read', 'write', 'create-repo', 'admin']
                        required: true
                        type: str
            add:
                description:
                    - Bitbucker Group permissions to add
                type: list
                elements: dict
                suboptions:
                    group:
                        description:
                            - The Name of the group to give permissions to
                        required: true
                        type: str
                    permission:
                        description: Permission to grant
                        choices: ['read', 'write', 'create-repo', 'admin']
                        required: true
                        type: str
            remove:
                description:
                    - Bitbucker Group permissions to remove
                type: list
                elements: str
    state:
        description: State the project role to ensure
        choices: ['present', 'absent']
        default: present
        type: str

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
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import BitbucketApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        key=dict(type='str', required=True, no_log=False),
        name=dict(type='str'),
        description=dict(type='str'),
        is_private=dict(type='bool', default=True),
        group_permission=dict(type='dict', default=None, options=dict(
            set=dict(type='list', elements='dict', options=dict(
                group=dict(type='str', required=True),
                permission=dict(type='str', required=True, choices=['read', 'write', 'create-repo', 'admin']),
            )),
            add=dict(type='list', elements='dict', options=dict(
                group=dict(type='str', required=True),
                permission=dict(type='str', required=True, choices=['read', 'write', 'create-repo', 'admin']),
            )),
            remove=dict(type='list', elements='str'),
        ), mutually_exclusive=[['set', 'add'], ['set', 'remove']]),
        state=dict(type='str',
                   default='present',
                   choices=['absent', 'present']),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = AnsibleAtlassianModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ('name',)),
        ]
    )

    # Parameters
    key = module.params['key']
    name = module.params['name']
    description = module.params['description']
    state = module.params['state']
    is_private = module.params['is_private']
    group_permission = module.params['group_permission']

    # Setup API
    api = BitbucketApi(module)

    # Get current state
    current_project = api.get(f"/projects/{ key }")

    # Delete
    if state == 'absent' and current_project is not None:
        result['changed'] = True
        new_project = {}
        if not module.check_mode:
            api.delete(f"/projects/{ key }")

    # Create
    if state == 'present' and current_project is None:
        result['changed'] = True

        new_project = dict(
            name=name,
            key=key,
            description=description,
            is_private=is_private,
        )
        if not module.check_mode:
            new_project = api.post("/projects", json=new_project)

    # Update
    if state == 'present' and current_project is not None:
        update = {}
        if name != current_project['name']:
            update['name'] = name
        if description and description != current_project['description']:
            update['description'] = description
        if is_private != current_project['is_private']:
            update['is_private'] = is_private

        if update:
            result['changed'] = True
            if not module.check_mode:
                new_project = api.put(f"/projects/{key}", json=update)
            else:
                new_project = current_project.copy()
                new_project.update(update)
        else:
            new_project = current_project.copy()
            new_project.update(update)

    if state == 'present' and group_permission is not None:
        if current_project is not None:
            current_group_permission = {p['group']['name']: p['permission'] for p in api.get(f"/projects/{key}/permissions-config/groups")['values']}
            current_project['group_permission'] = current_group_permission
        else:
            current_group_permission = {}
        new_project['group_permission'] = current_group_permission.copy()

        if group_permission['set']:
            for perm in group_permission['set']:
                if current_group_permission.get(perm['group'], None) != perm['permission']:
                    result['changed'] = True
                    new_project['group_permission'][perm['group']] = perm['permission']
                    if not module.check_mode:
                        api.put(f"/projects/{key}/permissions-config/groups/{perm['group']}", json=dict(permission=perm['permission']))
            for group in current_group_permission.keys():
                if group not in [p['group'] for p in group_permission['set']]:
                    del new_project['group_permission'][group]
                    if not module.check_mode:
                        api.delete(f"/projects/{key}/permissions-config/groups/{group}")

        if group_permission['add']:
            for perm in group_permission['add']:
                if current_group_permission.get(perm['group'], None) != perm['permission']:
                    result['changed'] = True
                    new_project['group_permission'][perm['group']] = perm['permission']
                    if not module.check_mode:
                        api.put(f"/projects/{key}/permissions-config/groups/{perm['group']}", json=dict(permission=perm['permission']))

        if group_permission['remove']:
            for perm in group_permission['remove']:
                if current_group_permission.get(perm['group'], None) is not None:
                    result['changed'] = True
                    del new_project['group_permission'][perm['group']]
                    if not module.check_mode:
                        api.delete(f"/projects/{key}/permissions-config/groups/{perm['group']}")

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_project, after=new_project)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
