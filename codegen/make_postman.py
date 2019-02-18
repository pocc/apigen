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
"""Generate Postman collection with OpenAPI 3 JSON.

For more information, read
    https://github.com/postmanlabs/openapi-to-postman
"""
import subprocess as sp
import shutil
import tempfile


def make_postman_collection(src, options):
    """Create a postman collection based on an OpenAPI3 JSON.

    Requires that node/npm be installed.
    Install openapi-to-postmanv2 to a temp directory,
        which is deleted when done.

    Args:
        src (str): Full path of OpenAPI3 JSON
        options (list): List of openapi2postman options. See
            https://github.com/postmanlabs/openapi-to-postman#options

    Raises:
        EnvironmentError: node is required. Quit if not found.
    """
    if not shutil.which('node'):
        raise EnvironmentError('Required node not found!')

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy(src, tmpdir)
        install_cmds = ['npm', 'install', '--prefix',
                        tmpdir, 'openapi-to-postmanv2']
        print("Installing openapi-to-postmanv2...")
        with sp.Popen(install_cmds, stdout=sp.PIPE, stderr=sp.PIPE) as sp_pipe:
            sp_pipe.communicate()

        openapi2postman = \
            'node_modules/openapi-to-postmanv2/bin/openapi2postmanv2.js'
        openapi2postman_cmds = ['node', openapi2postman, '-s', src, options]
        with sp.Popen(openapi2postman_cmds, stderr=sp.STDOUT) as sp_pipe:
            sp_pipe.communicate()

