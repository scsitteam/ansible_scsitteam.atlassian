# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_project_role

short_description: Manage Jira Project Roles

description:
    - Manage Jira Project Roles

options:
    name:
        description:
            - The Name of the project Role
        required: true
        type: str
    description:
        description:
            - The Description of the project Role. Required if state is present.
        type: str
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
# Create a project role
- name: Create Jira project Role
  jira_project_role:
    name: Ansible Dev
    description: Ansible Developer
'''

RETURN = '''
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str'),
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
            ('state', 'present', ('description',), True),
        ]
    )

    # Parameters
    name = module.params['name']
    description = module.params['description']
    state = module.params['state']

    # Setup API
    api = JiraPlatformApi(module)

    # Get current state
    current_project_role = api.get_project_role(name)

    # Delete
    if state == 'absent' and current_project_role is not None:
        result['changed'] = True
        new_project_role = {}
        if not module.check_mode:
            api.delete(f"/api/2/role/{current_project_role['id']}")

    # Create
    if state == 'present' and current_project_role is None:
        result['changed'] = True
        new_project_role = dict(
            name=name,
            description=description
        )
        if not module.check_mode:
            new_project_role = api.post("/api/2/role", payload=new_project_role)

    # Update
    if state == 'present' and current_project_role is not None and current_project_role["description"] != description:
        result['changed'] = True
        new_project_role = current_project_role.copy()
        new_project_role["description"] = description
        if not module.check_mode:
            new_project_role = api.post(f"/api/2/role/{current_project_role['id']}", payload=dict(description=description))

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_project_role, after=new_project_role)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
