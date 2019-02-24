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
"""Shared functions for testing modules."""
import io
from contextlib import redirect_stdout

DEFAULT_ARGS = {
    '--count': False,
    '--help': False,
    '--lang': [],
    '--options': None,
    '--show-generators': False,
    '--spec': [],
    '--verbose': False,
    '--verbosity': [],
    '--version': False
}


def get_stdout(function, args):
    """Get the stdout from a function."""
    f = io.StringIO()
    with redirect_stdout(f):
        function(args)
    return f.getvalue()
