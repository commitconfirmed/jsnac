import json
import jsonschema
import pytest

test_json_data = json.loads(open('data/example.json').read())
test_json_schema = json.loads(open('data/example.schema.json').read())

# Test the generated JSON schema is valid
def test_schema() -> None:
    jsonschema.Draft7Validator(test_json_schema)

# Test our example JSON data is valid against the generated schema
def test_all() -> None:
    jsonschema.validate(test_json_data, test_json_schema)

# Test the JSON schema with valid and invalid IPv4 addresses against our custom pattern
def test_ipv4_addresses() -> None:
    ipv4_definitions = test_json_schema['$defs']['ipv4']
    valid_ipv4_addresses = ["0.0.0.0", "255.255.255.255", "192.168.0.1"]
    invalid_ipv4_addresses = ["256.256.256.256", "192.168.0.256", "a.b.c.d", "192.168.0", "172.16.16.0.1"]
    for address in valid_ipv4_addresses:
        jsonschema.validate(address, ipv4_definitions)
    for address in invalid_ipv4_addresses:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(address, ipv4_definitions)