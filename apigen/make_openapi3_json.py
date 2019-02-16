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

}

[0] docstring with static parameters
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
            method = api_call['http_method'].lower()
            path, apicall_dict = get_apicall_dict(api_call)
            if path not in paths:
                paths[path] = {method: {}}

            paths[path][method] = apicall_dict

    return paths


def get_apicall_dict(api_call):
    """Get the api call JSON that is.

    This article was used for response syntax:
        https://swagger.io/docs/specification/describing-responses/
    """
    path_primitives = _vars.PATH_PRIMITIVES
    openapi_path = re.sub(r'[\[\{].*?[\}\]]', '{{{}}}', api_call['path'])

    apicall_success = str(api_call['successful_http_status'])
    api_method = api_call['http_method'].lower()
    last_non_param_word = openapi_path.replace('/{{{}}}', '').split('/')[-1]
    operation_id_snake_case = api_method + '_' + last_non_param_word

    operation_id = inf.camelize(operation_id_snake_case, False)
    apicall_json = {
        'description': api_call['description'],
        'operationId': operation_id,
        'summary': '',
        'parameters': [],
        'responses': {
            '400': {
                '$ref': '#/components/responses/400'
            },
            '404': {
                '$ref': '#/components/responses/404'
            },
            '500': {
                '$ref': '#/components/responses/500'
            }
        }
    }
    apicall_json['responses'][apicall_success] = {
        'description': 'Operation successful!'
    }

    if api_call['http_method'] in ['PUT', 'POST']:
        apicall_json['responses'][apicall_success]['content'] = {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/fixme'
                }
            }
        }
    elif api_call['http_method'] == 'GET':
        apicall_json['responses'][apicall_success]['content'] = {
            'type': 'array',
            'items': {
                    '$ref': '#/components/schemas/fixme'
            }
        }

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
    if path_params:
        last_param = path_params[-1]
        captialized_last_param = last_param[0].upper() + last_param[1:]
        apicall_json['operationId'] += 'By' + captialized_last_param

    openapi_path = openapi_path.format(*path_params)

    return openapi_path, apicall_json


def get_path_params(api_call_path):
    """Get the params from the path."""
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
    all_openapi_dict['paths'] = generate_path_dicts(api_docs)
    openapi_json_text = json.dumps(all_openapi_dict, indent=2)
    return openapi_json_text


var = converter_main()
