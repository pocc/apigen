# -*- coding: utf-8 -*-
# Copyright 2019 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""File a github issue."""
import http.client
import json
import re
import datetime
import distutils.version as versioning

import apigen


class GithubIssues:
    """Interface with Github Issues for apigen project."""
    def __init__(self):
        self.headers = {
            'Authorization': 'Basic cG9jYzo5Nzg5ODkwYmU4YThiYzZiZDc4'
                             'MDcwMmY4NGEwNmZlNzExZGJjY2Yw',
            'User-Agent': 'Merakygen'
        }

    def get_issues(self):
        """Get the issues for this project."""
        conn = http.client.HTTPSConnection('api.github.com')
        conn.request('GET', '/repos/pocc/apigen/issues',
                     headers=self.headers)
        resp = conn.getresponse()
        issues_text = resp.read().decode('utf-8')

        return issues_text

    def check_issue(self, api_primitive):
        """Check whether a new API primitive has an issue assigned."""
        issues_json = json.loads(self.get_issues())
        existing_issue_titles = [issue['title'] for issue in issues_json]
        new_issue_required = api_primitive not in existing_issue_titles
        if new_issue_required and is_up_to_date():
            print("INFO: API primitive not found, please create an issue:"
                  "\n\n\thttps://github.com/pocc/apigen/issues"
                  "\n\tTitle\tNew API primitive found: `" + api_primitive + "`"
                  "\n\tBody\tFound at " + str(datetime.datetime.utcnow()))


def is_up_to_date():
    """Check whether this program is out of date with github's."""
    base_url = 'raw.githubusercontent.com'
    route = '/pocc/apigen/master/apigen/__init__.py'
    conn = http.client.HTTPSConnection(base_url)
    conn.request('GET', route, headers={'User-Agent': 'Merakygen'})
    resp = conn.getresponse()
    init_text = resp.read().decode('utf-8')
    web_version = re.search(r'__version__ ?= ?\'([0-9.]*)\'', init_text)[1]

    up_to_date = versioning.StrictVersion(apigen.__version__) \
        >= versioning.StrictVersion(web_version)

    return up_to_date
