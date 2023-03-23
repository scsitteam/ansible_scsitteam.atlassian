# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_permission_scheme

short_description: Manage Jira permission scheme

description:
    - Manage Jira permission scheme

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
    permission:
        description:
            - Dictionary of Jira permissions.
        type: dict
        suboptions:
            administer_projects:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            browse_projects:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            manage_sprints_permission:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            servicedesk_agent:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            view_dev_tools:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            view_readonly_workflow:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            assignable_user:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            assign_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            close_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            create_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            edit_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            link_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            modify_reporter:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            move_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            resolve_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            schedule_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            set_issue_security:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            transition_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            manage_watchers:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            view_voter_and_Watchers:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            add_comments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_all_comments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_own_comments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            edit_all_comments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            edit_own_comments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            create_attachments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_all_attachments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_own_attachments:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_all_worklogs:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            delete_own_worklogs:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            edit_all_worklogs:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            edit_own_worklogs:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str
            work_on_issues:
                description: Allow to administrrate the project
                type: list
                elements: dict
                suboptions:
                    type:
                        description: Type of grant
                        type: str
                        choices: ['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']
                        required: true
                    value:
                        description: Value to Identify whi this permissions are granted to.
                        type: str

extends_documentation_fragment:
- scsitteam.atlassian.atlassian
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
- name: Set Jira Title
  jira_setting:
    atlassian_instance: example
    atlassian_username: user@example.com
    atlassian_password: secret
    settings:
      jira.title: Example Jira


- name: Reset Jira Title
  jira_setting:
    atlassian_instance: example
    atlassian_username: user@example.com
    atlassian_password: secret
    settings:
      jira.title:
'''

RETURN = '''
settings:
  description: Jira settings
  returned: success
  type: dict
  sample:
    {
      "jira.clone.prefix": "CLONE -",
      "jira.comment.collapsing.minimum.hidden": "4",
      "jira.date.picker.java.format": "d/MMM/yy",
      "jira.date.picker.javascript.format": "%e/%b/%y",
      "jira.date.time.picker.java.format": "dd/MMM/yy h:mm a",
      "jira.date.time.picker.javascript.format": "%e/%b/%y %I:%M %p"
    }
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


permission_options = dict(
    type=dict(type='str', required=True, choices=['anyone', 'applicationRole', 'assignee', 'group', 'groupCustomField']),
    value=dict(type='str')
)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present']),
        permission=dict(type='dict', default={}, options=dict(
            # Project permissions
            administer_projects=dict(type='list', elements='dict', options=permission_options),
            browse_projects=dict(type='list', elements='dict', options=permission_options),
            manage_sprints_permission=dict(type='list', elements='dict', options=permission_options),
            servicedesk_agent=dict(type='list', elements='dict', options=permission_options),
            view_dev_tools=dict(type='list', elements='dict', options=permission_options),
            view_readonly_workflow=dict(type='list', elements='dict', options=permission_options),
            # Issue permissions
            assignable_user=dict(type='list', elements='dict', options=permission_options),
            assign_issues=dict(type='list', elements='dict', options=permission_options),
            close_issues=dict(type='list', elements='dict', options=permission_options),
            create_issues=dict(type='list', elements='dict', options=permission_options),
            delete_issues=dict(type='list', elements='dict', options=permission_options),
            edit_issues=dict(type='list', elements='dict', options=permission_options),
            link_issues=dict(type='list', elements='dict', options=permission_options),
            modify_reporter=dict(type='list', elements='dict', options=permission_options),
            move_issues=dict(type='list', elements='dict', options=permission_options),
            resolve_issues=dict(type='list', elements='dict', options=permission_options),
            schedule_issues=dict(type='list', elements='dict', options=permission_options),
            set_issue_security=dict(type='list', elements='dict', options=permission_options),
            transition_issues=dict(type='list', elements='dict', options=permission_options),
            # Voters and watchers permissions
            manage_watchers=dict(type='list', elements='dict', options=permission_options),
            view_voter_and_Watchers=dict(type='list', elements='dict', options=permission_options),
            # Comments permissions
            add_comments=dict(type='list', elements='dict', options=permission_options),
            delete_all_comments=dict(type='list', elements='dict', options=permission_options),
            delete_own_comments=dict(type='list', elements='dict', options=permission_options),
            edit_all_comments=dict(type='list', elements='dict', options=permission_options),
            edit_own_comments=dict(type='list', elements='dict', options=permission_options),
            # Attachments permissions
            create_attachments=dict(type='list', elements='dict', options=permission_options),
            delete_all_attachments=dict(type='list', elements='dict', options=permission_options),
            delete_own_attachments=dict(type='list', elements='dict', options=permission_options),
            # Time tracking permissions
            delete_all_worklogs=dict(type='list', elements='dict', options=permission_options),
            delete_own_worklogs=dict(type='list', elements='dict', options=permission_options),
            edit_all_worklogs=dict(type='list', elements='dict', options=permission_options),
            edit_own_worklogs=dict(type='list', elements='dict', options=permission_options),
            work_on_issues=dict(type='list', elements='dict', options=permission_options),
        )),
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
    description = module.params['description']
    state = module.params['state']

    # Setup API
    api = JiraPlatformApi(module)

    current_scheme = next(filter(lambda p: p['name'] == name, api.get("/api/3/permissionscheme")['permissionSchemes']), None)
    result['current_scheme'] = current_scheme

    # Create
    if state == 'present' and current_scheme is None:
        result['changed'] = True
        new_scheme = dict(
            name=name,
            description=description,
        )
        if not module.check_mode:
            new_scheme = api.post("/api/3/permissionscheme", json=new_scheme)

    # Create
    if state == 'present' and current_scheme is not None:
        if current_scheme['description'] != description:
            result['changed'] = True

            if not module.check_mode:
                new_scheme = api.put(f"/api/3/permissionscheme/{current_scheme['id']}", json=dict(name=name, description=description))
            else:
                new_scheme = current_scheme.copy()
                new_scheme['description'] = description

    # Delete
    if state == 'absent' and current_scheme is not None:
        result['changed'] = True
        new_scheme = {}
        if not module.check_mode:
            api.delete(f"/api/3/permissionscheme/{current_scheme['id']}")

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=dict(scheme=current_scheme), after=dict(scheme=new_scheme))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
