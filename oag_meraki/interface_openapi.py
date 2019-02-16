"""Given an OpenAPI3 JSON, convert it to $lang of user choice.

Uses https://github.com/OpenAPITools/openapi-generator
"""
import subprocess as sp
import urllib.error as urlerr
import urllib.request as urlreq


def get_openapi_generator():
    """Get OpenAPI Generator and execute per language."""
    try:
        jarfile = 'http://central.maven.org/maven2/org/openapitools/open' \
                  'api-generator-cli/3.3.4/openapi-generator-cli-3.3.4.jar'
        urlreq.urlretrieve(jarfile, 'openapi-generator-cli.jar')
    except urlerr.URLError:
        raise ConnectionError("An internet connection is required.")


def generate_api_clients(*args):
    """Generate all of the API clients the user has specified."""
    for lang in args:
        cmd_list = ['java', '-jar', 'openapi-generator-cli.jar', 'generate',
                    '-i', 'merakiapi.json',
                    '-l', lang,
                    '-o', 'generated/' + lang]
        result = sp.check_output(cmd_list)
        print(result)
