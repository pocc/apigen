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
    mad-codegen [--lang <lang>...] [--spec <spec>...]
        [--options <options>] [--verbose]
    mad-codegen --show-generators
    mad-codegen --help
    mad-codegen [--version]

OPTIONS:
  -g, --show-generators     Show available languages on this system.
  -h, --help                Show this help dialog.
  -l, --lang                Generate $language API client. Can be
                            specified multiple times. Use --langs to
                            see the available languages on this system.
  -o, --options <options>   Options for language or postman generation. All
                            options should be enclosed in single/double quotes.
  -s, --spec <spec>...      Spec to output. Can be specified multiple times.
                            Available:
                                [openapi3, postman]
  -v, --version             Show the version and exit
  -V, --verbose             Include debugging information

DESCRIPTION:
    Create an API client in your $language.
    By default, will save the spec or module in the current working directory.

    A language or spec MUST be specified.

SEE ALSO:
  OpenAPI Generator: https://github.com/OpenAPITools/openapi-generator
"""
import sys
import subprocess as sp
import re

import docopt

import codegen


def get_cli_args():
    """CLI entry point"""
    args = docopt.docopt(__doc__)

    if args['--lang'] or args['--spec']:
        validate_targets(args)
        args = correct_fuzzy_args(args)
        return args
    else:
        parse_cli_args(args)
        sys.exit()


def validate_targets(args):
    """Validate whether the user inputted languages/specs are valid."""
    available_langs = re.findall(r'- (.*?)\n', get_openapi_generators())
    invalid_langs = set(args['--lang']).difference(set(available_langs))
    if invalid_langs:
        err_msg = "Valid languages on system: " + str(available_langs) + \
            "\nInvalid entered languages: " + str(invalid_langs)
        raise SyntaxWarning(err_msg)

    invalid_specs = set(args['--lang']).difference(set(codegen.__specs__))
    if invalid_specs:
        err_msg = "Valid languages on system: " + str(codegen.__specs__) + \
            "\nInvalid entered languages: " + str(invalid_specs)
        raise SyntaxWarning(err_msg)


def correct_fuzzy_args(args):
    """Change arguments to allow for fuzzy targets

    Corrections:
        'openapi' => 'openapi3'

    Args:
        args (dict): User entered arguments produced by docopt.
    Returns (dict):
        modified args
    """
    for index, spec in enumerate(args['--spec']):
        if spec == 'openapi':
            args['--spec'][index] = 'openapi3'
    return args


def parse_cli_args(args):
    """Act on args that don't require the main use of the program.

    Args:
        args (dict): User entered arguments produced by docopt.
    """
    if args['--version']:
        print(codegen.__version__)
    elif args['--show-generators']:
        print(get_openapi_generators())
    else:
        print("ERROR: Specify at least one language or spec.")

    sys.exit()


def get_openapi_generators():
    """Get the languages that OpenAPI Generator supports.

    Returns (str):
        Several paragraph lists of languages that OpenAPI Generator supports.
    """
    cmd_list = ['java', '-jar', 'openapi-generator-cli.jar']
    return sp.check_output(cmd_list).decode('utf-8').strip()
