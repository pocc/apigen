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
"""Test running python gateway.py with options."""
import unittest
import os


class TestIntegration(unittest.TestCase):
    """Test Meraki Apigen."""
    def setUp(self):
        """In case tests are started in the tests folder"""
        if os.path.basename(os.getcwd()).startswith('tests'):
            os.chdir('..')
        self.entry_point = 'gateway.py'

    def test_integration_python(self):
        """Test python generation."""

    def tearDown(self):
        """Remove any generated modules."""
