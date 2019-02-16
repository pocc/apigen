REGEX_MAC_ADDR = r'^([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})$'
REGEX_NETWORK = r'^[LN]_[\d]*$'
REGEX_SERIAL = r'^Q2[A-Z0-9]{2}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
REGEX_MX_SERVICES = r'^(?i)\bicmp|web|snmp\b$'
MIN_VLAN = 1
MAX_VLAN = 4094
MIN_PORT_NUMBER = 1
MAX_PORT_NUMBER = 48

# Prefer camelCase as the OpenAPI docs do. ' used per pythonic dict
PATH_PRIMITIVES = {
    'organizationId': {
        'name': 'organizationId',
        'description': 'Number that uniquely identifies an organization.'
            '\n ↳ get_orgs()',
        'example': 212406,
        'schema': {},
        'required': True

    },
    'networkId': {
        'name': 'networkId',
        'description': 'String that uniquely identifies a network'
            '\n ↳ get_networks_by_org_id(org_id)',
        'example': 'N_24329156',
        'schema': {},
        'required': True
    },
    'adminId': {
        'name': 'adminId',
        'description': 'Number that uniquely identifies an admin.'
            '\n ↳  get_admins_by_org_id(org_id)',
        'example': '545173',
        'schema': {},
        'required': True
    },
    'staticRouteId': {
        'name': 'staticRouteId',
        'description': 'UUID of static route' 
            '\n ↳ get_static_routes_by_network_id(network_id)',
        'example': 'd7fa4948-7921-4dfa-af6b-ae8b16c20c39',
        'schema': {},
        'required': True
    },
    'serial': {
        'name': 'serial',
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
        'description': 'Tag SM scope ID'
            '\n ↳ get_sm_named_tag_scopes_by_network_id(network_id, params)',
        'example': 1234,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'userId': {
        'name': 'userId',
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
        'description': 'Camera Analytics Zone ID'
            '\n ↳ get_analytics_zones_by_serial(serial)',
        'example': 1,
        'schema': {
            'type': 'integer'
        },
        'required': True
    },
    'bluetoothClientId': {
        'description': 'Bluetooth MAC'
            '\n ↳ get_bluetooth_clients_by_network_id(network_id, params)',
        'example': '00:11:22:33:44:55',
        'schema': {
            'type': 'string',
            'pattern': REGEX_MAC_ADDR
        },
        'required': True
    },
    'idOrMacOrIp': {
        'name': 'idOrMacOrIp',
        'description': 'Client ID or Mac or IP\n ↳ (multiple)',
        'example': '00:11:22:33:44:55',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'mac': {
        'name': 'mac',
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
        'description': 'Cisco Clarity Profile ID'
            '\n ↳ create_profile_clarity_by_network_id(network_id, params)',
        'example': 12345,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'appId': {
        'name': 'appId',
        'description': 'SM Cisco Polaris app ID'
              '\n ↳ get_app_polaris_by_network_id(network_id, params)',
        'example': 123456,
        'schema': {
            'type': 'integer',
            'format': 'int64'
        },
        'required': True
    },
    'smId': {
        'name': 'smId',
        'description': 'poke me',
        'example': 'poke me',
        'schema': {
            'type': 'string'
        },
        'required': True
    },
    'service': {
        'name': 'service',
        'description': 'MX Services'
            '\n ↳ get_firewalled_services_by_network_id(network_id)',
        'example': 'web',
        'schema': {
            'type': 'string',
            'pattern': REGEX_MX_SERVICES
        },
        'required': True
    },
    'vlanId': {
        'name': 'vlanId',
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
        'description': 'Beta endpoint lacks means of fetching ID.'
                       '\n ↳ get_switch_ports_by_serial(serial)',
        'example': 'poke me',
        'schema': {
            'type': 'string'
        },
        'required': True
    }
}

OPENAPI_START = """\
{
  "openapi": "3.0.0",
  "info": {
    "description": "Meraki API",
    "version": "0",
    "title": "Meraki API",
    "termsOfService": "https://meraki.cisco.com/support/#policies:eca",
    "contact": {
      "email": "rossbjacobs@gmail.com"
    },
    "license": {
      "name": "Apache 2.0",
      "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    }
  },
  "tags": [],
  "servers": [
    {
      "url": "http://api.meraki.com/api/{basePath}",
      "variables": {
        "basePath": {
          "default": "v0",
          "description": "Current version of the API"
        }
      }
    }
  ],
  "paths":"""

OPENAPI_END = """\
    "securitySchemes": {
      "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "X-Cisco-Meraki-API-Key"
      }
    }
  },
  "security": [
    {
      "ApiKeyAuth": []
    }
  ],
  "externalDocs": {
    "description": "Find out more about Meraki API docs",
    "url": "http://dashboard.meraki.com/api_docs"
  }
}"""
