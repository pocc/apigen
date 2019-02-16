"""Generate OpenAPI JSON.

More info on the standard can be found here:
https://github.com/OAI/OpenAPI-Specification


Example generated JSON:
{
  [0] "openapi": "3.0.0",
  ...

  [1] "paths": {
    "/organizations/{organizationId}/admins": {
      "get": {
        [2] "summary": "Get organization data",
  ...

  [3] "security": [
    {
      "ApiKeyAuth": []
    }
  ],
  ...
}

[0], [3] static docstrings prepended and appended to JSON respectively
[1] Via `generate_path_dicts`
[2] Via `get_apicall_dict`
"""
import json
import re
import webbrowser

import inflection as inf

import apigen._web as web
import apigen._vars as _vars
import apigen


def generate_path_dicts(api_docs):
    """Get the paths from the Meraki API docs JSON."""
    paths = {}
    for section in api_docs:
        for api_call in api_docs[section]:
            path = api_call['path']
            method = api_call['http_method'].lower()
            if path not in paths:
                paths[path] = {method: {}}
            paths[path][method] = get_apicall_dict(api_call)

    return paths


def get_apicall_dict(api_call):
    """Get the api call JSON that is."""
    path_primitives = _vars.PATH_PRIMITIVES
    apicall_json = {'parameters': []}
    path_params = get_path_params(api_call['path'])
    for path_param in path_params:
        if path_param not in path_primitives:
            webbrowser.open(apigen.__issues_url__ + '/new')
            err_msg = "Untracked API Primitive " + path_param + "!"  \
                      "\nPlease create an issue!"
            raise Exception(err_msg)

        apicall_json['parameters'] += [{
            path_param: path_primitives[path_param]
        }]
    return apicall_json


def get_path_params(api_call_path):
    """Get the params from the path.

    1. If the param is 'id', prepend the word before it
    2. If the prepend word is pluralized, singularize it
    3. If the param is snake_case, change to camel case
    """
    path_params = re.findall(r'[\[\{](.*?)[\]\}]', api_call_path)
    for idx, path_param in enumerate(path_params):

        if path_param.lower().startswith('id') or path_param == 'number':
            prepend_word_regex = r'\/([A-Za-z-_]*)\/[\[\{]' + path_param
            prepend_word = re.search(prepend_word_regex, api_call_path)[1]
            path_params[idx] = inf.singularize(prepend_word) + '_' + path_param
        path_params[idx] = inf.camelize(path_params[idx],
                                        uppercase_first_letter=False)

    return path_params


def converter_main():
    """Main function for the converter. This should be an essay, no calcs."""
    api_docs = web.fetch_apidocs_json()

    all_openapi_dict = _vars.OPENAPI_STUB
    all_openapi_dict['path'] = generate_path_dicts(api_docs)
    all_openapi_dict['components'] = {}
    all_openapi_dict['components']['securitySchemas'] = _vars.SECURITY_SCHEMES
    openapi_json_text = json.dumps(all_openapi_dict, indent=2, sort_keys=True)
    return openapi_json_text


print(converter_main())
