# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_setting

short_description: Manage Jira settings

description:
    - Manage Jira settings

options:
    settings:
        description:
            - The Jira settings as dictionary.
            - Settings set to None will be reset to there default value.
        required: true
        type: dict

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


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        settings=dict(type='dict', required=True),
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
    settings = module.params['settings']

    # Setup API
    api = JiraPlatformApi(module)

    current_settings = {ap['key']: ap['value'] for ap in api.get("/api/3/application-properties")}
    new_settings = current_settings.copy()
    result['settings'] = current_settings

    for key, value in settings.items():
        if key not in current_settings:
            current_settings[key] = api.get("/api/3/application-properties", params=dict(key=key))['defaultValue']

        if value is None:
            value = api.get("/api/3/application-properties", params=dict(key=key))['value']

        if current_settings.get(key, None) == value:
            continue

        result['changed'] = True
        new_settings[key] = value
        if not module.check_mode:
            api.put(f"/api/3/application-properties/{key}", json=dict(id=key, value=value))

    # Diff
    if result['changed'] and module._diff:
        result['diff'] = dict(before=current_settings, after=new_settings)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
