#!/usr/bin/python

# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = '''
---
module: confluence_space

short_description: Manage Confluence Space

description:
    - Manage a confluence space

options:
    key:
        description:
            - The Confluence Space key
        type: str
        required: true
    name:
        description:
            - The Name of the Confluence space
        type: str
        required: false
    description:
        description:
            - The Description of the Confluence space
        type: str
        required: false
    state:
        description:
            - The desired state of the space
        type: str
        required: false
        choices: [ present, absent ]
        default: present

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
        name=dict(type='str'),
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
        supports_check_mode=True
    )

    # Parameters
    key = module.params['key']
    name = module.params['name']
    description = module.params['description']
    state = module.params['state']

    # Setup API
    api = ConfluenceApi(module)

    # Get current state
    spaces = api.get("/api/v2/spaces", params={"description-format": "plain"})
    current_space = next(filter(lambda s: s['key'] == key, spaces['results']), None)

    result['space'] = current_space

    # Delete
    if state == 'absent' and current_space is not None:
        result['changed'] = True
        new_space = {}
        if not module.check_mode:
            api.delete(f"/rest/api/space/{current_space['id']}")

    # Create
    if state == 'present' and current_space is None:
        result['changed'] = True
        new_space = dict(
            key=key,
            name=name,
            description=dict(
                plain=dict(
                    value=description,
                    representation="PLAIN"
                )
            ),
        )
        if not module.check_mode:
            result['new_space'] = api.post("/rest/api/space", json=new_space)

    # Update
    if state == 'present' and current_space is not None:
        update = {}
        if name != current_space['name']:
            update['name'] = name
        if description and description != current_space['description']['plain']['value']:
            update['description'] = dict(
                plain=dict(
                    value=description,
                    representation="PLAIN"
                )
            )
        if update:
            result['changed'] = True
            if not module.check_mode:
                api.put(f"/rest/api/space/{key}", json=update)
            new_space = current_space.copy()
            new_space.update(update)

    result['current_space'] = current_space
    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_space, after=new_space)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
