# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_project_role_actor

short_description: Manage Jira Project Roles Actors

description:
    - Manage Jira Project Roles Actors

options:
    project_key:
        description:
            - The Jira project key of the project to act on.
        required: true
        type: str
    role:
        description:
            - The project role to grant or revoke.
        required: true
        type: str
    users:
        description: Users to grant the role to
        type: list
        elements: str
        aliases: [ 'user' ]
        default: []
    groups:
        description: Groups to grant the role to
        type: list
        elements: str
        aliases: [ 'group' ]
        default: []
    state:
        description: State of the project role for the subjects.
        choices: ['present', 'absent', 'pure']
        default: present
        type: str

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
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        project_key=dict(type='str', required=True, no_log=False),
        role=dict(type='str', required=True),
        users=dict(type='list', elements='str', aliases=['user'], default=[]),
        groups=dict(type='list', elements='str', aliases=['group'], default=[]),
        state=dict(type='str',
                   default='present',
                   choices=['absent', 'present', 'pure']),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = AnsibleAtlassianModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Setup API
    api = JiraPlatformApi(module)

    # Parameters
    project_key = module.params['project_key']
    role = api.get_project_role(project_key, module.params['role'])
    if not role:
        module.fail_json(f"Role '{module.params['role']}' not found.")
    state = module.params['state']

    # Get current state
    current_groups = {a['actorGroup']['groupId']: a['name'] for a in role['actors'] if a['type'] == 'atlassian-group-role-actor'}
    current_users = {a['actorUser']['accountId']: a['displayName'] for a in role['actors'] if a['type'] == 'atlassian-user-role-actor'}
    result['current_groups'] = current_groups
    result['current_users'] = current_users

    # Present
    if state == 'present' or state == 'pure':
        grant = dict(
            groupId=[api.get_group(g)['groupId'] for g in module.params['groups'] if g not in current_groups.values()],
            user=[api.get_user(u)['accountId'] for u in module.params['users'] if u not in current_users.values()],
        )

        if grant['groupId'] or grant['user']:
            result['changed'] = True
            if not module.check_mode:
                api.post(f"/api/2/project/{project_key}/role/{role['id']}", json=grant)

    # Absent
    if state == 'absent':
        revoke = dict(
            groupId=[id for id, name in current_groups.items() if name in module.params['groups']],
            user=[id for id, name in current_users.items() if name in module.params['users']],
        )

        if revoke['groupId'] or revoke['user']:
            result['changed'] = True
            if not module.check_mode:
                api.delete(f"/api/2/project/{project_key}/role/{role['id']}", params=revoke)

    # Pure
    if state == 'pure':
        revoke = dict(
            groupId=[id for id, name in current_groups.items() if name not in module.params['groups']],
            user=[id for id, name in current_users.items() if name not in module.params['users']],
        )

        if revoke['groupId'] or revoke['user']:
            result['changed'] = True
            if not module.check_mode:
                api.delete(f"/api/2/project/{project_key}/role/{role['id']}", params=revoke)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
