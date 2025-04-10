# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_project

short_description: Manage Jira Project

description:
    - Manage a Jira Project

options:
    key:
        description:
            - The Jira project key
        required: true
        type: str
    name:
        description:
            - The Name of the Jira project.
        type: str
    description:
        description:
            - The Description of the Jira project
        type: str
    lead:
        description:
            - The Username of the Jira Project lead.
        type: str
    permission_scheme:
        description:
            - The name of the permission scheme used to create a new project.
            - Does not update the active permision scheme.
        type: str
    notification_scheme:
        description:
            - The name of the notification scheme used to create a new project.
            - Does not update the active notification scheme.
        type: str
    template:
        description: Project template to use
        default: com.pyxis.greenhopper.jira:gh-simplified-basic
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
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        key=dict(type='str', required=True, no_log=False),
        name=dict(type='str'),
        description=dict(type='str'),
        lead=dict(type='str'),
        permission_scheme=dict(type='str'),
        notification_scheme=dict(type='str'),
        state=dict(type='str',
                   default='present',
                   choices=['absent', 'present']),
        template=dict(type='str', default='com.pyxis.greenhopper.jira:gh-simplified-basic')
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
            ('state', 'present', ('name', 'lead'), True),
        ]
    )

    # Parameters
    key = module.params['key']
    name = module.params['name']
    description = module.params['description']
    state = module.params['state']
    lead = module.params['lead']
    permission_scheme_name = module.params['permission_scheme']
    notification_scheme_name = module.params['notification_scheme']
    template = module.params['template']

    # Setup API
    api = JiraPlatformApi(module)

    # Get lead
    if lead:
        leaduser = api.get(f"/api/3/user/search?query={ lead }")
        if len(leaduser) != 1:
            module.fail_json(msg="Error finding Lead user", **result)
        leaduser = leaduser[0]

    # Get permission scheme
    if permission_scheme_name:
        permission_schemes = api.get("/api/3/permissionscheme")['permissionSchemes']
        permission_scheme = next(filter(lambda p: p['name'] == permission_scheme_name, permission_schemes), None)
        if permission_scheme is None:
            module.fail_json(msg=f"Error finding permission scheme '{permission_scheme_name}'",
                             permission_schemes=[p['name'] for p in permission_schemes], **result)
    else:
        permission_scheme = None

    # Get notification scheme
    if notification_scheme_name:
        startat = 0
        while True:
            page = api.get(f"/api/3/notificationscheme?startAt={startat}")
            notification_schemes = page['values']
            notification_scheme = next(filter(lambda p: p['name'] == notification_scheme_name, notification_schemes), None)
            if notification_scheme is not None:
                break
            if page['isLast']:
                module.fail_json(msg=f"Error finding permission scheme '{notification_scheme_name}'",
                                 notification_scheme=[p['name'] for p in notification_schemes], **result, page=page)
            startat += page['maxResults']
    else:
        notification_scheme = None

    # Get current state
    current_project = api.get(f"/api/2/project/{ key }")

    # Delete
    if state == 'absent' and current_project is not None:
        issues = api.get(f"/api/2/search?jql=project%20%3D%20{ key }")
        if issues['total'] > 0:
            module.fail_json(msg="The Project is not empty", issues=[i['key'] for i in issues['issues']], **result)

        result['changed'] = True
        new_project = {}
        if not module.check_mode:
            api.delete(f"/api/2/project/{ key }")

    # Create
    if state == 'present' and current_project is None:
        result['changed'] = True

        payload = dict(
            key=key,
            name=name,
            description=description,
            leadAccountId=leaduser['accountId'],
            projectTypeKey="software",
            projectTemplateKey=template,
        )
        if permission_scheme:
            payload['permissionScheme'] = permission_scheme['id']
        if notification_scheme:
            payload['notificationScheme'] = notification_scheme['id']
        result['new_project'] = payload
        if not module.check_mode:
            result['new_project'] = api.post("/api/2/project", json=payload)

    # Update
    if state == 'present' and current_project is not None:
        payload = {}
        if current_project['name'] != name:
            payload['name'] = name
        if description and current_project['description'] != description:
            payload['description'] = description
        if leaduser['accountId'] != current_project['lead']['accountId']:
            payload['leadAccountId'] = leaduser['accountId']

        if payload:
            result['changed'] = True
            if not module.check_mode:
                new_project = api.put(f"/api/2/project/{key}", json=payload)
            else:
                new_project = current_project.copy()
                new_project.update(payload)

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_project, after=new_project)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
