# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: bitbucket_group

short_description: Manage Bitbucket Groups

description:
    - Manage a Bitbucket Groups

options:
    name:
        description:
            - The Name of the Bitbucket Group.
        required: true
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
'''

RETURN = '''
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import BitbucketLegacyApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
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
    )

    # Parameters
    name = module.params['name']
    state = module.params['state']

    # Setup API
    api = BitbucketLegacyApi(module)

    # Get current state
    current_group = {g['name']: g for g in api.get("/groups/{workspace_id}/")}.get(name, None)
    result['current_group'] = current_group

    # Delete
    if state == 'absent' and current_group is not None:
        result['changed'] = True
        new_group = {}
        if not module.check_mode:
            api.delete(f"/groups/{{workspace_id}}/{ name }")

    # Create
    if state == 'present' and current_group is None:
        result['changed'] = True
        result['msg'] = 'Create Group'

        new_group = dict(
            name=name,
        )
        if not module.check_mode:
            new_group = api.post("/groups/{workspace_id}/", data=new_group)

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_group, after=new_group)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
