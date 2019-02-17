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
"""Module to govern interaction with the web."""
import json
import os
import time
import urllib.request
import socket


def get_apidocs_webpage(url):
    """Get API docs webpage and return pagetext."""
    with urllib.request.urlopen(url) as response:
        text = response.read().decode('utf-8')

    return text


def fetch_apidocs_json():
    """Get all Meraki API calls from the official docs.

    * apidocs json is shipped with projcet at merakygen/static/api.json
    * This will be used if there is no network connection, but
      may be out-of-date.
    * If this program is run multiple times, try to cache it to
      save on network requests and speed.
    """
    docs_url = 'https://dashboard.meraki.com/api_docs'
    api_json_name = 'meraki_api.json'
    try:
        # If a local copy has been created in the last 24 hours, use it.
        if os.path.exists(api_json_name) and \
                time.time() - os.stat(api_json_name).st_mtime < 86400:
            api_docs = get_json_str_from_file(api_json_name)
        else:
            text = get_apidocs_webpage(docs_url)
            # Get the json by splitting the pagetext at json beginning and end.
            lower_split = text.split("window.allApisJson = ")[1]
            all_api_docs_str = lower_split.split(";\n  </script>")[0]
            api_docs = json.loads(all_api_docs_str)
            # Write the json so a cached version is now available.
            with open(api_json_name, 'w') as file_obj:
                file_obj.write(json.dumps(api_docs, indent=2))

    except socket.gaierror:
        # If there's a network problem.
        api_docs = get_json_str_from_file('../static/meraki_api.json')

    return api_docs


def get_json_str_from_file(filename):
    """Open a file and get its JSON as a dict."""
    with open(filename) as file_obj:
        return json.loads(file_obj.read())

fetch_apidocs_json()