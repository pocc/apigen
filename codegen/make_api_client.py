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
"""Given an OpenAPI3 JSON, convert it to $lang of user choice.

Uses https://github.com/OpenAPITools/openapi-generator
"""
import subprocess as sp
import os
import urllib.error as urlerr
import urllib.request as urlreq


def download_openapi_generator():
    """Download OpenAPI Generator if it's not cached."""
    if not os.path.exists('openapi-generator-cli.jar'):
        try:
            jarfile = 'http://central.maven.org/maven2/org/openapitools/open' \
                      'api-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar'
            urlreq.urlretrieve(jarfile, 'openapi-generator-cli.jar')
        except urlerr.URLError:
            raise ConnectionError("An internet connection is required.")


def generate_api_clients(langs, openapi_location):
    """Generate all of the API clients the user has specified.

    Args:
        langs (list): All of the user entered output options.
        openapi_location (str): Where the openapi json is stored.
    """
    for lang in langs:
        cmd_list = ['java', '-jar', 'openapi-generator-cli.jar', 'generate',
                    '-i', openapi_location,
                    '-l', lang,
                    '-o', 'generated/' + lang]
        result = sp.check_output(cmd_list)
        print(result)
