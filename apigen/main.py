# -*- coding: utf-8 -*-
"""Main function."""
import subprocess as sp
import re

import apigen._cli as cli
import apigen.make_api_client as api_client


def main():
    """Main function."""
    check_requirements()
    user_langs = cli.get_cli_args()['--lang']
    available_langs = get_languages()
    invalid_langs = set().difference(set(available_langs))
    if invalid_langs:
        err_msg = "Valid languages on system: " + available_langs + \
            "\nInvalid entered languages: " + str(invalid_langs)
        raise SyntaxWarning(err_msg)

    generate_openapi_json()
    api_client.get_openapi_generator()
    api_client.generate_api_clients(user_langs)


def check_requirements():
    """Check the requirements
    
    Requirements:
        * java > 1.8
    """
    check_java_version()

    print('...Requirements satisfied!')


def generate_openapi_json():
    """Generate an Open API 3.0.0 compatible json."""


def check_java_version():
    """Verify whether Java version is correct."""
    required_java_version = 1.8
    java_version = get_java_version()
    if java_version < required_java_version:
        raise Exception("Required Java 1.8+ not found.")


def get_java_version():
    """Return the system java version."""
    cmd_list = ['java', '-version']
    version_text = str(sp.check_output(cmd_list, stderr=sp.STDOUT))
    if 'version' not in version_text:
        raise Exception("Java not found. Reinstall and try again.")
    version = re.search(r'"([\d]*\.[\d]*)\.[\d]*_', str(version_text))[1]
    
    return float(version)


def get_languages():
    """Get the languages that OpenAPI Generator supports.

    :returns list
    """
    cmd_list = 'java -jar openapi-generator-cli.jar langs'.split(' ')
    avail_languages_str = sp.check_output(cmd_list).decode('utf-8').strip()
    languages_str = avail_languages_str.split(': ')[1]
    languages_list = languages_str[1:-1].split(', ')  # Remove '[', ']'

    return languages_list


if __name__ == '__main__':
    main()
