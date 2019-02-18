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
import tempfile

import inflection as inf

import codegen._web as web
import codegen._vars as _vars
import codegen.utils as utils
import codegen


def generate_path_dicts(api_docs):
    """Get the paths from the Meraki API docs JSON."""
    paths = {}
    all_schemas = {}
    operation_ids = []
    all_api_calls = []
    for section in api_docs:
        for api_call in api_docs[section]:
            all_api_calls += [api_call]
            # Add 2 API calls if there are 2 paths.
            if api_call['alternate_path']:
                api_call['path'] = api_call['alternate_path']
                all_api_calls += [api_call]

    for api_call in all_api_calls:
        method = api_call['http_method'].lower()
        path, schemas, apicall_dict = get_apicall_dict(api_call)

        # Ensure no operation id duplicates by adding a number to the end
        count = 2
        unique_operation_id = apicall_dict['operationId']
        while unique_operation_id in operation_ids:
            unique_operation_id = apicall_dict['operationId'] + str(count)
            count += 1
        apicall_dict['operationId'] = unique_operation_id
        operation_ids += [unique_operation_id]
        if path not in paths:
            paths[path] = {method: {}}
        all_schemas = {**all_schemas, **schemas}

        paths[path][method] = apicall_dict

    return paths, all_schemas


def get_apicall_dict(api_call):
    """Get the api call JSON that is.

    This article was used for response syntax:
        https://swagger.io/docs/specification/describing-responses/
    """
    path_primitives = _vars.PATH_PRIMITIVES
    openapi_path = re.sub(r'[\[\{].*?[\}\]]', '{{{}}}', api_call['path'])
    schemas = {}

    apicall_success = str(api_call['successful_http_status'])
    api_method = api_call['http_method'].lower()
    last_non_param_word = openapi_path.replace('/{{{}}}', '').split('/')[-1]
    last_non_param_word = inf.camelize(last_non_param_word)
    operation_id = api_method + last_non_param_word
    apicall_success_message = api_call['http_method'] + ' Successful!'
    apicall_json = {
        'description': api_call['description'],
        'operationId': operation_id,
        'summary': '',
        'parameters': [],
        'responses': {
            apicall_success: {'description': apicall_success_message},
            '301': {'$ref': '#/components/responses/301'},
            '302': {'$ref': '#/components/responses/302'},
            '307': {'$ref': '#/components/responses/302'},
            '400': {'$ref': '#/components/responses/400'},
            '404': {'$ref': '#/components/responses/404'},
            '500': {'$ref': '#/components/responses/500'}
        }
    }

    # POST /networks/{networkId}/devices/{serial}/remove returns 204 wrongly
    has_put_post_success = apicall_success in ['200', '201']
    if api_call['http_method'] in ['PUT', 'POST'] and has_put_post_success:
        apicall_json['responses'][apicall_success]['content'] = {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/' + last_non_param_word
                }
            }
        }

    elif api_call['http_method'] == 'GET' and apicall_success == '200':
        pass
        # Assuming that it's fine to skip providing a response schema for gets
        """
        array_schema_name = 'ArrayOf' + last_non_param_word
        apicall_json['responses'][apicall_success]['content'] = {
            'application/json': {
              'schema': {
                '$ref': '#/components/schemas/' + array_schema_name
                }
            }
        }
        
        schemas[array_schema_name] = {
            'type': 'array',
            'items': {
                '$ref': '#/components/schemas/' + last_non_param_word
            }
        }

        # Creates a dummy value for object type if not assigned eleswhere
        if last_non_param_word not in schemas:
            schemas[last_non_param_word] = {
                'type': 'string',
                'properties': 
            }
        """

    has_query_params = 'params' in api_call and api_call['params']
    if has_query_params:
        all_params = [param['name'] for param in api_call['params']]
        required_params = [param['name'] for param in api_call['params']
                           if 'optional' not in param['description']]
        schemas[last_non_param_word] = {
            "required": required_params,
            "properties": {}
        }
        for p_index, param in enumerate(all_params):
            param_dict = api_call['params'][p_index]
            nested = 'params' in param_dict
            if nested:
                nested_params = [param for param in param_dict['params']]
                nested_params_names =[param['name'] for param in nested_params]
                nested_params_dict = {}
                for np_index, nested_param in enumerate(nested_params):
                    nested_param_dict = param_dict['params'][np_index]
                    nested_params_dict[nested_param['name']] = {
                        'type': 'string',
                        'description': nested_param_dict['description']
                    }
                schemas[last_non_param_word]['properties'][param] = {
                    'type': 'array',
                    'description': param_dict['description'],
                    'items': {
                        '$ref': '#/components/schemas/' + param
                    }
                }
                schemas[param] = {
                    'type': 'object',
                    'required': nested_params_names,
                    'properties': nested_params_dict
                }
            else:
                schemas[last_non_param_word]['properties'][param] = {
                    'type': 'string',
                    'description': param_dict['description']
                }

    path_params = get_path_params(api_call['path'])
    for path_param in path_params:
        if path_param not in path_primitives:
            issue = utils.GithubIssues()
            is_issue_required = issue.check_issue(path_param)
            if is_issue_required:
                message = "Press i & return to submit an issue on Github." + \
                          "\nPress return to continue."
                if input(message).lower() == 'i':
                    webbrowser.open(codegen.__issues_url__ + '/new')

        apicall_json['parameters'] += [path_primitives[path_param]]
    if path_params:
        last_param = path_params[-1]
        captialized_last_param = last_param[0].upper() + last_param[1:]
        apicall_json['operationId'] += 'By' + captialized_last_param

    openapi_path = openapi_path.format(*path_params)

    return openapi_path, schemas, apicall_json


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


def make_spec(save_locally):
    """Main function for the converter.

    Args:
        save_locally (bool): Whether to save the openapi json locally
            or in a temp folder.
    """
    api_docs = web.fetch_apidocs_json()

    all_openapi_dict = _vars.OPENAPI_STUB
    all_openapi_dict['paths'], gen_schemas = generate_path_dicts(api_docs)
    all_schemas = {**all_openapi_dict['components']['schemas'], **gen_schemas}
    all_openapi_dict['components']['schemas'] = all_schemas

    openapi_json_text = json.dumps(all_openapi_dict, indent=2, sort_keys=True)

    filename = 'openapi3.json'
    if save_locally:
        filename = 'generated_clients/' + filename
    else:
        filename = tempfile.TemporaryDirectory().name + filename
    with open(filename, 'w') as openapi_file:
        openapi_file.write(openapi_json_text)

    return filename
