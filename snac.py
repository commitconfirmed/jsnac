import json
import os
import logging

# Set up logging to the terminal, with colors
def my_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def infer_schema(data):  
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
                case 'choice':
                    if 'jsnac_choices' not in data:
                        log.error(f"jsnac_choices key is required for jsnac_type: choice.")
                        schema['enum'] = [ "Error" ]	
                        schema['title'] = "Error"
                        schema['description'] = "No jsnac_choices key provided"
                    else:    
                        schema['enum'] = data['jsnac_choices']
                        schema['title'] = "Custom Choice"
                        schema['description'] = "Custom Choice (enum) \n Choices: " + ", ".join(data['jsnac_choices'])
                case _:
                    log.error(f"Invalid jsnac_type: {data['jsnac_type']}, defaulting to null")
                    schema['type'] = "null"
                    schema['title'] = "Error"
                    schema['description'] = "Invalid jsnac_type defined"
        # If not, simply continue inferring the schema
        else:
            schema['type'] = "object"
            schema['properties'] = {k: infer_schema(v) for k, v in data.items()}
    elif isinstance(data, list):
        if len(data) > 0:
            schema['type'] = "array"
            schema['items'] = infer_schema(data[0])
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

def json_to_schema(json_file_path, schema_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    log.debug(f"Inferring schema for: \n {json.dumps(data, indent=4)}")
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "JSNAC Created Schema",
        "description": "The below schema was created by JSNAC (https://github.com/commitconfirmed/jsnac)",
        "$defs": {
            "ipv4": {
                "type": "string",
                "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])$",
                "title": "IPv4 Address",
                "description": "IPv4 address (String) \n Format: xxx.xxx.xxx.xxx"
            },
            # IPv6 regex pattern from https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
            "ipv6": {
                "type": "string",
                "pattern": "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
                "title": "IPv6 Address",
                "description": "Short IPv6 address (String) \n Accepts both full and short form addresses, link-local addresses, and IPv4-mapped addresses"
            },
            "ipv4_cidr": {
                "type": "string",
                "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",
                "title": "IPv4 CIDR",
                "description": "IPv4 CIDR (String) \n Format: xxx.xxx.xxx.xxx/xx"
            },
            # I'll fix this to inlcude more types later
            "ipv6_cidr": {
                "type": "string",
                "pattern": "^([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}/[0-9]{1,3}$",
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
                "pattern": "^([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$",
                "title": "Domain Name",
                "description": "Domain name (String) \n Format: example.com"
            },
            # String is a default type, but in this instance we restict it to alphanumeric + special characters with a max length of 255
            "string": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9!@#$%^&*()_+-\\{\\}|:;\"'<>,.?/]{1,255}$",
                "title": "String",
                "description": "Alphanumeric string with special characters (String) \n Max length: 255"
            },
        },
        "type": "object",
        "additionalProperties": False,
        "properties": infer_schema(data)["properties"]
    }

    with open(schema_file_path, 'w') as schema_file:
        json.dump(schema, schema_file, indent=4)

if __name__ == "__main__":
    log = my_logger()
    json_file_path = "test.json"
    schema_file_path = "test-schema.json"
    json_to_schema(json_file_path, schema_file_path)