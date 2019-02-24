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
"""Parse HTML."""
import json
import logging
import re

import codegen._cache as cache
import codegen._hardcoded

LOGGER = logging.getLogger()


def parse_apidocs_json(docs_url, html_filename):
    """Get all Meraki API calls from the official docs."""
    try:
        cache.download_file(docs_url, html_filename)
    except ConnectionError:
        LOGGER.warning("Not connected to the internet. "
                       "Using potentially stale API Docs source.")
        with open('../assets/meraki_api.json') as file_obj:
            return json.loads(file_obj.read())

    api_json_name = 'meraki_api.json'

    if cache.is_file_cached(api_json_name):
        api_docs = codegen._cache.load_json(api_json_name)
    else:
        cached_html_filepath = cache.get_filepath(html_filename)
        with open(cached_html_filepath) as myfile:
            pagetext = myfile.read()
        apidocs_json_regex = r'allApisJson = (.*?);\n'
        api_docs = json.loads(re.search(apidocs_json_regex, pagetext)[1])
        cache.cache_file(api_json_name, json.dumps(api_docs, indent=2))

    return api_docs
