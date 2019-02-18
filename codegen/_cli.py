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
"""Meraki API Docs Code Generator

USAGE:
    mad-codegen [--lang <lang>...] [--spec <spec>...] [--option <option>...]

OPTIONS:
  -l, --lang <lang>...      Language to output. Can be specified multiple times
                            Available: []
  -s, --spec <spec>...      Spec to output. Can be specified multiple times.
                            Available: [openapi3, postman]
  -o, --option <option>...  Options for language or postman generation.


DESCRIPTION:
    Create an API client in your $language.
    By default, will save the spec or module in the current working directory.

    If no options are specified, default is to output openapi3 json and quit.

SEE ALSO:
  OpenAPI Generator: https://github.com/OpenAPITools/openapi-generator
"""
import docopt


def get_cli_args():
    """CLI entry point"""
    args = docopt.docopt(__doc__)
    no_options_specified = not args['--lang'] and not args['--spec']
    if no_options_specified:
        args['--spec'] = 'openapi3'

    return args
