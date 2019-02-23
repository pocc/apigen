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
"""Utilities that codegen uses."""
import datetime
import distutils.version
import http.client
import json
import logging
import re

import codegen

LOGGER = logging.getLogger()


class GithubIssues:
    """Interface with Github Issues for mad-codegen project."""
    def __init__(self):
        self.headers = {
            'Authorization': 'Basic cG9jYzo5Nzg5ODkwYmU4YThiYzZiZDc4'
                             'MDcwMmY4NGEwNmZlNzExZGJjY2Yw',
            'User-Agent': 'Merakygen'
        }

    def get_issues(self):
        """Get the issues for this project."""
        conn = http.client.HTTPSConnection('api.github.com')
        conn.request('GET', '/repos/pocc/mad-codegen/issues',
                     headers=self.headers)
        resp = conn.getresponse()
        issues_text = resp.read().decode('utf-8')

        return issues_text

    def check_issue(self, api_primitive):
        """Check whether a new API primitive has an issue assigned.

        Args:
            api_primitive (str): A Meraki API path parameter
        Returns (bool):
            Whether there is a new path parameter that requires an issue
        """
        issues_json = json.loads(self.get_issues())
        existing_issue_titles = [issue['title'] for issue in issues_json]
        new_issue_required = api_primitive not in existing_issue_titles \
            and self.is_up_to_date()
        if new_issue_required:
            print("INFO: API primitive not found. "
                  "This means new API endpoints have been released."
                  "\nPlease create an issue:"
                  "\n\n\thttps://github.com/pocc/mad-codegen/issues"
                  "\n\tTitle\tNew API primitive found: `" + api_primitive + "`"
                  "\n\tBody\tFound at " + str(datetime.datetime.utcnow()))

        return new_issue_required

    def is_up_to_date(self):
        """Check whether this program is out of date with github's.

        Returns (bool):
            Whether this program is out of date with masters' version.
        """
        base_url = 'raw.githubusercontent.com'
        route = '/pocc/mad-codegen/master/mad-codegen/__init__.py'
        conn = http.client.HTTPSConnection(base_url)
        conn.request('GET', route, headers=self.headers)
        resp = conn.getresponse()
        init_text = resp.read().decode('utf-8')
        web_version = re.search(r'__version__ ?= ?\'([0-9.]*)\'', init_text)[1]

        up_to_date = distutils.version.StrictVersion(codegen.__version__) \
            >= distutils.version.StrictVersion(web_version)

        return up_to_date


def log_ext_program_output(program_name, program_output):
    """Other programs return log text via Popen. Format that and log it.

    Log it as debug as it is verbose and mostly not relevant to operation.

    Args:
        program_output (str): Output of another program
        program_name (str): Name of the program being called
    """
    if 'ERROR' in program_output:
        err_line = re.search(r'\n(.*?ERROR.*?)\n', program_output).group(1)
        raise RuntimeError(program_name + ' produced error: ' + str(err_line))

    output_line_start = '\n\t> [' + program_name + '] > '
    program_output = program_output.replace('\n\n', '\n')
    formatted_text = re.sub(r'\n([\S ])', output_line_start + '\\1',
                            program_output)
    LOGGER.debug('`' + program_name + '` STDOUT >' +
                 output_line_start + formatted_text)
