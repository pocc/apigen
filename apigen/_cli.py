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
"""
mad_codegen --lang <lang>...

OPTIONS:
  -l, --lang <lang>     Output language. Can be specified multiple times.

SEE ALSO:
  OpenAPI Generator: https://github.com/OpenAPITools/openapi-generator
"""
import docopt


def get_cli_args():
    """CLI entry point"""
    return docopt.docopt(__doc__)
