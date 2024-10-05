import os
import logging
import json
import yaml

class SchemaInferer:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

    # Take in JSON data and confirm it is valid JSON
    def add_json(self, json_data):
        try:
            load_json_data = json.loads(json_data)
            self.log.debug(f"JSON content: \n {json.dumps(load_json_data, indent=4)}")
            self.data = load_json_data
        except json.JSONDecodeError as e:
            self.log.error(f"Invalid JSON data: {e}")
            raise Exception(f"Invalid JSON data: {e}")

    # Take in YAML data, confirm it is valid YAML and then and convert it to JSON
    def add_yaml(self, yaml_data):
        try:
            load_yaml_data = yaml.safe_load(yaml_data)
            self.log.debug(f"YAML content: \n {load_yaml_data}")
        except yaml.YAMLError as e:
            self.log.error(f"Invalid YAML data: {e}")
            raise Exception(f"Invalid YAML data: {e}")
        json_dump = json.dumps(load_yaml_data, indent=4)
        json_data = json.loads(json_dump)
        self.log.debug(f"JSON content: \n {json_dump}")
        self.data = json_data

    def build(self):
        # Check if the data has been added
        if not hasattr(self, 'data'):
            self.log.error("No data has been added to the schema inferer")
            raise Exception("No data has been added to the schema inferer. Use add_json or add_yaml to add data.")
        else:
            data = self.data

        self.log.debug(f"Building schema for: \n {json.dumps(data, indent=4)}")
        # Currently using draft-07 until vscode $dynamicRef support is added (https://github.com/microsoft/vscode/issues/155379)
        # Feel free to replace this with https://json-schema.org/draft/2020-12/schema if not using vscode
        schema = {
            "$schema": "https://json-schema.org/draft-07/schema",
            "title": "JSNAC Created Schema",
            "description": "The below schema was created by JSNAC (https://github.com/commitconfirmed/jsnac)",
            "$defs": {
                "ipv4": {
                    "type": "string",
                    "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])$",
                    "title": "IPv4 Address",
                    "description": "IPv4 address (String) \n Format: xxx.xxx.xxx.xxx"
                },
                # IPv6 regex pattern from https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
                "ipv6": {
                    "type": "string",
                    "pattern": "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
                    "title": "IPv6 Address",
                    "description": "Short IPv6 address (String) \n Accepts both full and short form addresses, link-local addresses, and IPv4-mapped addresses"
                },
                "ipv4_cidr": {
                    "type": "string",
                    "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",
                    "title": "IPv4 CIDR",
                    "description": "IPv4 CIDR (String) \n Format: xxx.xxx.xxx.xxx/xx"
                },
                "ipv6_cidr": {
                    "type": "string",
                    "pattern": "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/([6-9][0-9]|1[0-2][0-8])$",
                    "title": "IPv6 CIDR",
                    "description": "Full IPv6 CIDR (String) \n Format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx"
                },
                "ipv4_prefix": {
                    "type": "string",
                    "title": "IPv4 Prefix",
                    "pattern": "^/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",
                    "description": "IPv4 Prefix (String) \n Format: /xx between 0 and 32"
                },
                "ipv6_prefix": {
                    "type": "string",
                    "title": "IPv4 Prefix",
                    "pattern": "^/([6-9][0-9]|1[0-2][0-8])$",
                    "description": "IPv6 prefix (String) \n Format: /xx between 64 and 128"
                },
                "domain": {
                    "type": "string",
                    "pattern": "^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$",
                    "title": "Domain Name",
                    "description": "Domain name (String) \n Format: example.com"
                },
                # String is a default type, but in this instance we restict it to alphanumeric + special characters with a max length of 255
                "string": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9!@#$%^&*()_+-\\{\\}|:;\"'<>,.?/ ]{1,255}$",
                    "title": "String",
                    "description": "Alphanumeric string with special characters (String) \n Max length: 255"
                },
            },
            "type": "object",
            "additionalProperties": False,
            "properties": self.infer_properties(data)["properties"]
        }
        return json.dumps(schema, indent=4)

    # Infer the properties of the data passed in, this function will call itself recursively to infer nested properties
    def infer_properties(self, data):
        schema = {}
        if isinstance(data, dict):
            # Check if the dictionary has a jsnac_type key in it, then we know we can use our custom schema definitions
            if 'jsnac_type' in data:
                match data['jsnac_type']:
                    case 'ipv4':
                        schema['$ref'] = "#/$defs/ipv4"
                    case 'ipv6':
                        schema['$ref'] = "#/$defs/ipv6"
                    case 'ipv4_cidr':
                        schema['$ref'] = "#/$defs/ipv4_cidr"
                    case 'ipv6_cidr':
                        schema['$ref'] = "#/$defs/ipv6_cidr"
                    case 'ipv4_prefix':
                        schema['$ref'] = "#/$defs/ipv4_prefix"
                    case 'domain':
                        schema['$ref'] = "#/$defs/domain"
                    case 'string':
                        schema['$ref'] = "#/$defs/string"
                    case 'pattern':
                        if 'jsnac_pattern' not in data:
                            self.log.error(f"jsnac_pattern key is required for jsnac_type: pattern.")
                            schema['type'] = "null"
                            schema['title'] = "Error"
                            schema['description'] = "No jsnac_pattern key provided"
                        else:
                            schema['type'] = "string"
                            schema['pattern'] = data['jsnac_pattern']
                            schema['title'] = "Custom Pattern"
                            schema['description'] = "Custom Pattern (regex) \n Pattern: " + data['jsnac_pattern']
                    case 'choice':
                        if 'jsnac_choices' not in data:
                            self.log.error(f"jsnac_choices key is required for jsnac_type: choice.")
                            schema['enum'] = ["Error"]
                            schema['title'] = "Error"
                            schema['description'] = "No jsnac_choices key provided"
                        else:
                            schema['enum'] = data['jsnac_choices']
                            schema['title'] = "Custom Choice"
                            schema['description'] = "Custom Choice (enum) \n Choices: " + ", ".join(data['jsnac_choices'])
                    case _:
                        self.log.error(f"Invalid jsnac_type: ({data['jsnac_type']}), defaulting to null")
                        schema['type'] = "null"
                        schema['title'] = "Error"
                        schema['description'] = "Invalid jsnac_type (" + data['jsnac_type'] + ") defined"
            # If not, simply continue inferring the schema
            else:
                schema['type'] = "object"
                schema['properties'] = {k: self.infer_properties(v) for k, v in data.items()}
        elif isinstance(data, list):
            if len(data) > 0:
                schema['type'] = "array"
                schema['items'] = self.infer_properties(data[0])
            else:
                schema['type'] = "array"
                schema['items'] = {}
        elif isinstance(data, str):
            schema['type'] = "string"
        elif isinstance(data, int):
            schema['type'] = "integer"
        elif isinstance(data, float):
            schema['type'] = "number"
        elif isinstance(data, bool):
            schema['type'] = "boolean"
        else:
            schema['type'] = "null"
        return schema

