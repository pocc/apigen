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
        [--options <options>] [--verbose | --verbosity <level>]
    mad-codegen --count
    mad-codegen --show-generators
    mad-codegen --help
    mad-codegen --version

OPTIONS:
  -c, --count               Print the number of API calls that exist now.
  -g, --show-generators     Show available languages on this system.
  -h, --help                Show this help dialog.
  -l, --lang <lang>         Generate $language API client. Can be
                            specified multiple times. Use --langs to
                            see the available languages on this system.
  -o, --options <options>   Options for language or postman generation. All
                            options should be enclosed in single/double quotes.
  -s, --spec <spec>         Spec to output. Can be specified multiple times.
                            Available:
                                [openapi3, postman]
  -v, --verbose             Alias for --verbosity INFO
      --verbosity <level>   One of (CRITICAL, ERROR, WARNING, INFO, DEBUG)
                            Default is WARNING. For more info:
                                https://docs.python.org/3/library/logging.html#logging-levels
  -V, --version             Show the version and exit

DESCRIPTION:
    Create an API client in your $language.
    By default, will save the spec or module in the current working directory.

    Requires `java`. For postman export, requires `node`.

    A language or spec MUST be specified.

SEE ALSO:
  OpenAPI Generator: https://github.com/OpenAPITools/openapi-generator
"""
import distutils.version
import logging
import os
import re
import subprocess as sp
import sys

import docopt

import codegen
import codegen._hardcoded
import codegen._parse_html as parse_html
import codegen.make_api_client

LOGGER = logging.getLogger()


def get_cli_args(args=None):
    """CLI entry point

    Args:
        args (list): List of system args for unit tests.
    """
    if not args:
        args = docopt.docopt(__doc__)
    set_log_level(args)
    log_msg = "`docopt` ARGS >\n" + str(args)
    LOGGER.debug(log_msg)

    check_java_version()

    if args['--lang'] or args['--spec']:
        if not os.path.exists('generated_clients'):
            os.makedirs('generated_clients')
        args = correct_fuzzy_args(args)
        verify_valid_specs(args['--spec'])

        return args['--spec'], args['--lang'], args['--options']

    parse_cli_args(args)
    return None


def check_java_version():
    """Verify whether Java version is correct.

    Requirements:
        * java >= 1.8
    """
    required_java_version = '1.8'
    cmd_list = ['java', '-version']
    version_text = str(sp.check_output(cmd_list, stderr=sp.STDOUT))
    if 'version' not in version_text:
        raise Exception("Java not found. Reinstall and try again.")
    java_version = re.search(r'"([\d]*\.[\d]*)\.[\d]*_', str(version_text))[1]
    has_required_java_version = distutils.version.StrictVersion(java_version) \
        >= distutils.version.StrictVersion(required_java_version)
    if not has_required_java_version:
        raise Exception("Required Java 1.8+ not found.")

    LOGGER.info('✓ java >= 1.8 satisfied.')


def set_log_level(args):
    """Set the log level according to user supplied args."""
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s [%(module)s] '
                                  '%(levelname)s %(message)s')
    logging_out = logging.StreamHandler(sys.stdout)
    logging_err = logging.StreamHandler(sys.stderr)
    logging_out.setLevel(logging.WARNING)
    logging_out.setLevel(logging.WARNING)
    logging_out.setFormatter(formatter)
    logging_err.setFormatter(formatter)
    LOGGER.addHandler(logging_out)
    LOGGER.addHandler(logging_err)

    no_verbosity_selected = not args['--verbose'] and not args['--verbosity']
    if no_verbosity_selected:
        LOGGER.setLevel(logging.WARNING)  # default
    elif args['--verbose']:
        LOGGER.setLevel('INFO')
    else:  # Some --verbosity <level> entered
        if args['--verbosity'] in list(log_levels):
            LOGGER.setLevel(log_levels[args['--verbosity']])
            log_msg = 'Setting verbosity to ' + args['--verbosity']
            LOGGER.info(log_msg)
        else:
            print('ERROR: Invalid verbosity level.')
            sys.exit()


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


def verify_valid_specs(entered_specs):
    """Verify whether the spec entered is supported by MAD CodeGen."""
    invalid_specs = set(entered_specs).difference(codegen.__specs__)
    if invalid_specs:
        err_msg = "Valid specs: " + str(codegen.__specs__) + \
            "\nInvalid entered specs: " + str(invalid_specs)
        raise SyntaxWarning(err_msg)


def parse_cli_args(args):
    """Act on args that don't require the main use of the program.

    Args:
        args (dict): User entered arguments produced by docopt.
    """
    if args['--version']:
        print(codegen.__version__)
    elif args['--show-generators']:
        openapi_obj = codegen.make_api_client.OpenApiGenerator()
        generator_lists = openapi_obj.get_avail_generators()
        print(generator_lists)
    elif args['--count']:
        docs_url = codegen._hardcoded.MERAKI_API_DOCS_LINK
        apidocs = parse_html.parse_apidocs_json(docs_url, 'meraki_api.html')
        count = 0
        for section in apidocs:
            for path in apidocs[section]:
                if 'path' in path and path['path']:
                    count += 1
                if 'alternate_path' in path and path['alternate_path']:
                    count += 1
        print(count)
    else:
        print("ERROR: Specify at least one language or spec.")
