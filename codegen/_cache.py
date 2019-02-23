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
"""Abstract a local cache."""
import json
import logging
import os
import subprocess as sp
import time
import urllib.request
import urllib.error

import codegen._utils as utils

LOGGER = logging.getLogger(__name__)


def cache_file(file_name, file_contents):
    """Make a file in the cache directory if it doesn't exist."""
    cached_filename = '.cache/' + file_name
    if not os.path.exists('.cache'):
        os.makedirs('.cache')
    with open(cached_filename, 'w') as file_obj:
        file_obj.write(file_contents)

    return cached_filename


def load_json(filename):
    """Open a file and get its JSON as a dict."""
    cached_filename = '.cache/' + filename
    if is_file_cached(cached_filename):
        with open(cached_filename) as file_obj:
            return json.loads(file_obj.read())


def is_file_cached(filename):
    """Check whether file is cached.

    Args:
        filename (str): The file to be checked.
    Returns (bool):
        Whether the file is cached or not.
    """
    return os.path.exists(filename)


def get_filepath(filename):
    """Get the full filepath of a cached file.

    Args:
        filename (str): The file to get the full path for
    Returns (str):
        Full file path.
    Raises:
        FileNotFoundError: If the file has not been found in the cache.
    """
    cached_filename = '.cache/' + filename
    if is_file_cached(cached_filename):
        return os.getcwd() + '/' + cached_filename

    raise FileNotFoundError("File " + filename + " not found in cache.")


def get_node_module(module):
    """Download a node module if it's not in cache."""
    cache_dir = os.getcwd() + "/.cache/"
    target_module = '.cache/node_modules/' + module
    already_have_target_module = os.path.exists(target_module)
    if already_have_target_module:
        LOGGER.info('Using cached openapi-to-postmanv2')
    else:
        log_msg = "Downloading " + module + " to " + cache_dir
        LOGGER.info(log_msg)
        install_cmds = ['npm', 'install', '--prefix',
                        cache_dir, module]
        with sp.Popen(install_cmds, stdout=sp.PIPE,
                      stderr=sp.STDOUT) as sp_pipe:
            LOGGER.info('Starting npm install')
            result = sp_pipe.communicate()[0].decode('utf-8')
            utils.log_ext_program_output('npm', result)


def download_file(url, filename):
    """Download a file and if it doesn't already exist in .cache/"""
    cached_filename = os.getcwd() + '/.cache/' + filename

    if file_cached_within_24hrs(cached_filename):
        LOGGER.info('Using cached ' + cached_filename)
    else:
        try:
            urllib.request.urlretrieve(url, cached_filename)
            log_msg = 'Successfully downloaded ' + cached_filename
            LOGGER.info(log_msg)
        except urllib.error.URLError as err:
            err_msg = "An internet connection is required " \
                      "to download required assets"
            raise ConnectionError(err, err_msg)

    return cached_filename


def file_cached_within_24hrs(filename):
    """Has it been less than 24 hours since the file was last cached?

    Args:
        filename (str): The filename to check.
    Returns (bool):
        Whether the cached file is less than 24 hours old, if there is one
    """
    if is_file_cached(filename):
        seconds_in_a_day = 86400
        seconds_since_last_updated = time.time() - os.stat(filename).st_mtime
        return seconds_in_a_day > seconds_since_last_updated

    return False
