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
"""Main function."""
import codegen._cli as cli
import codegen.make_api_client
import codegen.make_openapi3_json
import codegen.make_postman as postman


def main():
    """Main function."""
    args = cli.get_cli_args()
    if args:
        specs, langs, options = args
        save__locally = 'openapi3' in specs
        openapi3_path = codegen.make_openapi3_json.make_spec(save__locally)

        if 'postman' in specs:
            postman.make_postman_collection(openapi3_path, options)

        if langs:
            openapi_gen = codegen.make_api_client.OpenApiGenerator()
            openapi_gen.generate_api_clients(langs, openapi3_path)


if __name__ == '__main__':
    main()
