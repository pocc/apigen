"""Generate OpenAPI JSON."""
import json
import re

import merakygen._web as web
import merakygen._vars as vars


def generate_paths(api_docs):
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
    apicall_json = {'parameters': []}
    path_params = re.findall(r'[\[\{](.*?)[\]\}]', api_call['path'])
    for path_param in path_params:
        apicall_json['parameters'] += [{
            path_param: vars.PATH_PRIMITIVES[path_param]
        }]

    return apicall_json


def converter_main():
    """Main function for the converter. This should be an essay, no calcs."""
    api_docs = web.fetch_apidocs_json()
    paths = generate_paths(api_docs)
    paths_text = json.dumps(paths, indent=4, sort_keys=True)
    openapi_json_text = vars.OPENAPI_START + paths_text + vars.OPENAPI_END
    return openapi_json_text


print(converter_main())
