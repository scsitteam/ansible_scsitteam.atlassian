# Copyright (c) 2023, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: jira_info

short_description: Get Jira Infos

description:
    - Manage a Jira Project

extends_documentation_fragment:
- scsitteam.atlassian.atlassian
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
- name: Get Jira Server Info
  jira_info:
    atlassian_instance: ansiblecollectiontest
  register: result
'''

RETURN = '''
baseurl:
    description: The base URL of the Jira instance.
    returned: success
    type: str
buildDate:
    description: The timestamp when the Jira version was built.
    returned: success
    type: str
buildNumber:
    description: The build number of the Jira version.
    returned: success
    type: str
deploymentType:
    description: The type of server deployment. This is always returned as Cloud.
    returned: success
    type: str
scmInfo:
    description: The unique identifier of the Jira version.
    returned: success
    type: str
serverTitle:
    description: The name of the Jira instance.
    returned: success
    type: str
version:
    description: The version of Jira.
    returned: success
    type: str
versionNumbers:
    description: The major, minor, and revision version numbers of the Jira version.
    returned: success
    type: list
'''

from ansible_collections.scsitteam.atlassian.plugins.module_utils.module import AnsibleAtlassianModule
from ansible_collections.scsitteam.atlassian.plugins.module_utils.api import JiraPlatformApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict()

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

    # Setup API
    api = JiraPlatformApi(module)

    # Get Status
    status = api.get("/api/3/serverInfo")
    result.update(status)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
