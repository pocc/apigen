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
"""Dicts and strings for use by other modules."""
import codegen

# OpenAPI doesn't like boundaries, so no (?i)\b ... \b for case insensitivity.
REGEX_MAC_ADDR = r'^([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})$'
REGEX_NETWORK = r'^[LN]_[\d]*$'
REGEX_SERIAL = r'^Q2[A-Z0-9]{2}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
REGEX_MX_SERVICES = r'^icmp|web|snmp|ICMP|WEB|SNMP$'
MIN_VLAN = 1
MAX_VLAN = 4094
MIN_PORT_NUMBER = 1
MAX_PORT_NUMBER = 48
# Noting that Meraki does not have a Terms of Service for its API
# Using the Terms of Use for the website as the API is a part of it
MERAKI_TERMS_OF_USE_URL = 'https://meraki.cisco.com/support/#policies:tou'

# Prefer camelCase as the OpenAPI docs do. Use ' as quote per python dict
PATH_PRIMITIVES = {
    'organizationId': {
        'name': 'organizationId',
        'in': 'path',
        'description': 'Number that uniquely identifies an organization.'
                       '\n ↳ get_orgs()',
        'example': 212406,
        'schema': {
            'type': 'integer',
        },
        'required': True

    },
    'networkId': {
        'name': 'networkId',
        'in': 'path',
        'description': 'String that uniquely identifies a network'
                       '\n ↳ get_networks_by_org_id(org_id)',
        'example': 'N_24329156',
        'schema': {
            'type': 'string',
            'pattern': REGEX_NETWORK
        },
        'required': True
    },
    'adminId': {
        'name': 'adminId',
        'in': 'path',
        'description': 'Number that uniquely identifies an admin.'
                       '\n ↳  get_admins_by_org_id(org_id)',
        'example': '545173',
        'schema': {
            'type': 'integer',
        },
        'required': True
    },
    'srId': {
        'name': 'srId',
        'in': 'path',
        'description': 'UUID of static route'
                       '\n ↳ get_static_routes_by_network_id(network_id)',
        'example': 'd7fa4948-7921-4dfa-af6b-ae8b16c20c39',
        'schema': {
            'type': 'string',
            'format': 'uuid'
        },
        'required': True
    },
    'serial': {
        'name': 'serial',
        'in': 'path',
        'description': 'All caps Meraki serial number.'
                       '\n ↳ get_devices_by_network_id(network_id)',
        'example': 'Q234-ABCD-5678',
        'schema': {
            'type': 'string',
            'pattern': REGEX_SERIAL
        },
        'required': True
    },
    'namedTagScopeId': {
        'name': 'namedTagScopeId',
        'in': 'path',
        'description': 'Tag SM scope ID\n ↳ get_sm_named_'
                       'tag_scopes_by_network_id(network_id, params)',
        'example': 1234,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'userId': {
        'name': 'userId',
        'in': 'path',
        'description': 'User ID used for SM'
                       '\n↳ get_sm_users_by_network_id(network_id, params)',
        'example': 1284392014819,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'ssidNumber': {
        'name': 'ssidNumber',
        'in': 'path',
        'description': 'Positional number of the SSID in the list'
                       '\n ↳ get_ssids_by_network_id(network_id)',
        'example': 2,
        'schema': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 14
        },
        'required': True
    },
    'zoneId': {
        'name': 'zoneId',
        'in': 'path',
        'description': 'Camera Analytics Zone ID'
                       '\n ↳ get_analytics_zones_by_serial(serial)',
        'example': 1,
        'schema': {
            'type': 'integer',
            'minimum': 0
        },
        'required': True
    },
    'bluetoothClientId': {
        'name': 'bluetoothClientId',
        'in': 'path',
        'description': 'Bluetooth MAC\n ↳ get_bluetooth_clients_'
                       'by_network_id(network_id, params)',
        'example': '00:11:22:33:44:55',
        'schema': {
            'type': 'string',
            'pattern': REGEX_MAC_ADDR
        },
        'required': True
    },
    'clientIdOrMacOrIp': {
        'name': 'clientIdOrMacOrIp',
        'in': 'path',
        'description': 'Client ID or Mac or IP\n ↳ (multiple)',
        'example': '00:11:22:33:44:55',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'mac': {
        'name': 'mac',
        'in': 'path',
        'description': 'Client MAC'
                       '\n ↳ get_clients_by_serial(serial, params)',
        'example': '00:11:22:33:44:55',
        'schema': {
            'type': 'string',
            'pattern': REGEX_MAC_ADDR
        },
        'required': True
    },
    'configTemplateId': {
        'name': 'configTemplateId',
        'in': 'path',
        'description': 'Like network ID, but for config templates.'
                       '\n↳ get_config_templates_by_org_id(org_id)',
        'example': 'N_24329156',
        'schema': {
            'type': 'string',
            'pattern': REGEX_NETWORK
        },
        'required': True
    },
    'httpServerId': {
        'name': 'httpServerId',
        'in': 'path',
        'description': 'Webhook HTTP server ID. See '
                       'https://documentation.meraki.com/z'
                       'General_Administration/Other_Topics/Webhooks'
                       '\n ↳ get_http_servers_by_network_id(network_id)',
        'example': 'poke me',
        'schema': {
            'type': 'string',
        },
        'required': True
    },
    'webhookTestId': {
        'name': 'webhookTestId',
        'in': 'path',
        'description': 'ID of webhook test sent to your HTTP server. See'
                       'https://documentation.meraki.com/z'
                       'General_Administration/Other_Topics/Webhooks'
                       '\n ↳ create_http_servers_webhook_tests_by_network_id'
                       '(network_id, params)',
        'example': 'poke me',
        'schema': {
            'type': 'string',
        },
        'required': True
    },
    'merakiAuthUserId': {
        'name': 'merakiAuthUserId',
        'in': 'path',
        'description': 'Splash or RADIUS user hash',
        'example': 'aGlAaGkuY29t'
                   '\n ↳ get_meraki_auth_users_by_network_id(network_id)',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'phoneAnnouncementId': {
        'name': 'phoneAnnouncementId',
        'in': 'path',
        'description': '↳ get_phone_announcements_by_network_id(network_id)',
        'example': 1284392014819,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'phoneCallgroupId': {
        'name': 'phoneCallgroupId',
        'in': 'path',
        'description': '↳ get_phone_callgroups_by_network_id(network_id)',
        'example': 178449602133687616,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'phoneConferenceRoomId': {
        'name': 'phoneConferenceRoomId',
        'in': 'path',
        'description': '↳ get_networks_by_org_id(org_id)',
        'example': 563512903374733359,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'contactId': {
        'name': 'contactId',
        'in': 'path',
        'description': 'Phone contact ID'
                       '\n ↳ get_phone_assignments_by_network_id(network_id)',
        'example': 823,
        'schema': {
            'type': 'integer'
        },
        'required': True
    },
    'requestId': {
        'name': 'requestId',
        'in': 'path',
        'description': 'PII request ID'
                       '\n ↳ get_pii_requests_by_network_id(network_id)',
        'example': 1234,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'samlRoleId': {
        'name': 'samlRoleId',
        'in': 'path',
        'description': 'ID unique to SAML User'
                       '\n ↳ get_saml_roles_by_org_id(org_id)',
        'example': 'TEdJIEN1c3RvbWVy',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'clientId': {
        'name': 'clientId',
        'in': 'path',
        'description': 'Client ID Hash'
                       '\n ↳ get_clients_by_serial(serial)',
        'example': 'k74272e',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'profileId': {
        'name': 'profileId',
        'in': 'path',
        'description': 'Cisco Clarity Profile ID\n ↳ create_profile_'
                       'clarity_by_network_id(network_id, params)',
        'example': 12345,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'appId': {
        'name': 'appId',
        'in': 'path',
        'description': 'SM Cisco Polaris app ID\n ↳ get_app_'
                       'polaris_by_network_id(network_id, params)',
        'example': 123456,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'smId': {
        'name': 'smId',
        'in': 'path',
        'description': 'poke me',
        'example': 'poke me',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'service': {
        'name': 'service',
        'in': 'path',
        'description': 'MX Services\n ↳ get_firewalled_services_'
                       'by_network_id(network_id)',
        'example': 'web',
        'schema': {
            'type': 'string',
            'pattern': REGEX_MX_SERVICES
        },
        'required': True
    },
    'vlanId': {
        'name': 'vlanId',
        'in': 'path',
        'description': 'VLAN number'
                       '\n ↳ get_vlans_by_network_id(network_id)',
        'example': 1234,
        'schema': {
            'type': 'integer',
            'minimum': MIN_VLAN,
            'maximum': MAX_VLAN
        },
        'required': True
    },
    'switchPortNumber': {
        'name': 'switchPortNumber',
        'in': 'path',
        'description': '↳ get_switch_ports_by_serial(serial)',
        'example': 7,
        'schema': {
            'type': 'integer',
            'minimum': MIN_PORT_NUMBER,
            'maximum': MAX_PORT_NUMBER
        },
        'required': True
    },
    'targetGroupId': {
        'name': 'targetGroupId',
        'in': 'path',
        'description': 'Beta endpoint lacks means of fetching ID.'
                       '\n ↳ get_switch_ports_by_serial(serial)',
        'example': 'poke me',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'groupPolicyId': {
        'name': 'groupPolicyId',
        'in': 'path',
        'description': 'Id that uniquely identifies a group policy'
                       '\n ↳ poke me',
        'example': 'poke me',
        'schema': {
            'type': 'string'
        },
        'required': True
    }
}


def make_json_schema_call(call_name):
    """Generate schema JSON as it is so common."""
    return {
        'application/json': {
            'schema': {
                '$ref': '#/components/schemas/' + call_name
            }
        }
    }


OPENAPI_STUB = {
    "openapi": "3.0.0",
    "info": {
        "title": 'Generated Meraki API',
        "description": "Generated from Meraki API Docs."
                       "\n" + codegen.__url__,
        "version": codegen.__version__,
        "termsOfService": MERAKI_TERMS_OF_USE_URL,
        "contact": {
            "name": codegen.__author__,
            "email": codegen.__author_email__
        },
        "license": {
            "name": codegen.__license__,
            "url": codegen.__license_url__
        }
    },
    "tags": [],
    "servers": [
        {
            "url": "http://dashboard.meraki.com/api/{basePath}",
            "variables": {
                "basePath": {
                    "default": "v0",
                    "description": "Current version of the API"
                }
            }
        }
    ],
    "security": [
        {
            "ApiKeyAuth": []
        }
    ],
    "externalDocs": {
        "description": "Find out more about Meraki API docs",
        "url": "http://dashboard.meraki.com/api_docs"
    },
    'components': {
        'responses': {
            '301': {
                'description': 'Permanent Redirect.',
                'content': make_json_schema_call('Error')
            },
            '302': {
                'description': 'Temporary Redirect.',
                'content': make_json_schema_call('Error')
            },
            '400': {
                'description': 'Bad request. Check input params.',
                'content': make_json_schema_call('Error')
            },
            '404': {
                'description': 'Resource not found',
                'content': make_json_schema_call('Error')
            },
            '500': {
                'description': 'Server error.',
                'content': make_json_schema_call('Error')
            }
        },
        'schemas': {
            'Error': {
                'type': 'object',
                'properties': {
                    'code': {
                        'type': 'string'
                    },
                    'message': {
                        'type': 'string'
                    }
                },
                'required': [
                    'code',
                    'message'
                ]
            },
            # POST /networks/{networkId}/unbind
            # Returns a network dict so redirect to appropriate schema
            'Unbind': {
                '$ref': '#/components/schemas/Networks'
            }
        },
        'securitySchemes': {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-Cisco-Meraki-API-Key"
            }
        }
    }
}
