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
"""Test _cli.py."""

import unittest
import subprocess as sp
import sys
import os

from tests import get_stdout, DEFAULT_ARGS
import codegen._cli as cli

KNOWN_API_CALL_COUNT = 218


class TestCli(unittest.TestCase):
    """Test Meraki Apigen."""
    def setUp(self):
        """In case tests are started in the tests folder"""
        if os.path.basename(os.getcwd()).startswith('tests'):
            os.chdir('..')
        self.cmd_list = ['python3', os.getcwd() + '/gateway.py']

    def test_count_python(self):
        """Test --count. This will fail when API calls are added (intended)."""
        testargs = dict(DEFAULT_ARGS)
        testargs['--count'] = True
        count_output = get_stdout(cli.get_cli_args, testargs)
        self.assertEqual(KNOWN_API_CALL_COUNT, int(count_output))

    def test_help_python(self):
        """Test python generation."""

    def tearDown(self):
        """Remove any generated modules."""
