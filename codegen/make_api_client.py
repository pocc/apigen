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
"""Given an OpenAPI3 JSON, convert it to $lang of user choice."""
import logging
import subprocess as sp
import re

import codegen._cache as cache
import codegen._hardcoded as hardcoded
import codegen._utils as utils

LOGGER = logging.getLogger(__name__)


class OpenApiGenerator:
    """Uses https://github.com/OpenAPITools/openapi-generator

    Inclusivity metric:
        * Uses openapi-generator-cli
        * Helps generate an API Client
    """
    def __init__(self):
        self.openapi_cli_name = 'openapi-generator-cli.jar'
        openapi_cli_filepath = cache.download_file(hardcoded.OPENAPI_DL_LINK,
                                                   self.openapi_cli_name)
        self.openapi_cli_cmds = ['java', '-jar', openapi_cli_filepath]

    def verify_valid_languages(self, input_langs):
        """Validate whether the user entered supported languages."""
        available_langs = re.findall(r'- (.*?)\n', self.get_avail_generators())
        invalid_langs = set(input_langs).difference(set(available_langs))
        if invalid_langs:
            err_msg = "Valid languages on system: " + str(available_langs) + \
                "\nInvalid entered languages: " + str(invalid_langs)

            raise SyntaxWarning(err_msg)

    def get_avail_generators(self):
        """Get the languages that this OpenAPI Generator supports.

        Returns (str):
            Several paragraph-lists of OpenAPI Generator supported languages.
        """
        cmd_list = self.openapi_cli_cmds + ['list']
        sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.STDOUT)
        return sp_pipe.communicate()[0].decode('utf-8').strip()

    def generate_api_clients(self, langs, openapi_json):
        """Generate all of the API clients the user has specified.

        Args:
            langs (list): All of the user entered output options.
            openapi_json (str): Path to OpenAPI3 JSON
        """
        self.verify_valid_languages(langs)
        cmd_list = self.openapi_cli_cmds + ['generate', '-i', openapi_json]

        for lang in langs:
            log_msg = "Creating API client for " + lang
            LOGGER.info(log_msg)
            cmd_list += ['-g', lang, '-o', 'generated_clients/' + lang]
            result = sp.check_output(cmd_list).decode('utf-8')
            utils.log_ext_program_output('openapi-generator-cli', result)

        log_msg = 'Generated files for ' + str(langs) + \
                  ' can be found in generated_clients/'
        LOGGER.info(log_msg)
