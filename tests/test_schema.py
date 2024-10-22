import json
from pathlib import Path

import jsonschema
import pytest

# Load our example JSON data and schema
test_json_file = Path("data/example.json")
test_schema_file = Path("data/example.schema.json")
with test_json_file.open() as f:
    test_json_data = json.loads(f.read())
    f.close()
with test_schema_file.open() as f:
    test_json_schema = json.loads(f.read())
    f.close()


# Test the generated JSON schema is valid
def test_schema() -> None:
    jsonschema.Draft7Validator(test_json_schema)
    assert True


# Test our example JSON data is valid against the generated schema
def test_all() -> None:
    jsonschema.validate(test_json_data, test_json_schema)
    assert True


# Test the JSON schema with valid IPv4 addresses against our custom definition
@pytest.mark.parametrize("address", ["0.0.0.0", "255.255.255.255", "192.168.0.1"])
def test_valid_ipv4_addresses(address) -> None:
    ipv4_definitions = test_json_schema["$defs"]["ipv4"]
    jsonschema.validate(address, ipv4_definitions)
    assert True


# Test the JSON schema with invalid IPv4 addresses, make sure they raise a ValidationError
@pytest.mark.parametrize(
    "address",
    ["256.256.256.256", "192.168.0.256", "a.b.c.d", "192.168.0", "172.16.16.0.1"],
)
def test_invalid_ipv4_addresses(address) -> None:
    ipv4_definitions = test_json_schema["$defs"]["ipv4"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv4_definitions)


# Test the JSON schema with valid IPv6 addresses
@pytest.mark.parametrize(
    "address",
    [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:0:0:0:8a2e:370:7334",
        "2001:db8::8a2e:370:7334",
        "2001:db8::1",
        "2001:db8::",
        "::1",
    ],
)
def test_valid_ipv6_addresses(address) -> None:
    ipv6_definitions = test_json_schema["$defs"]["ipv6"]
    jsonschema.validate(address, ipv6_definitions)
    assert True


# Test the JSON schema with some invalid IPv6 addresses, make sure they raise a ValidationError
@pytest.mark.parametrize(
    "address",
    [
        "10.0.0.1",
        ":1:",
        "2001:0db8:85a3:0000:0000:8a2e:0370" "2001:0db8:85a3:0000:0000:8a2e:0370:7334:1234",
        "2001:0db8:85a3::0:0::8a2e:0370:7334",
        "2001:gb8::1",
    ],
)
def test_invalid_ipv6_addresses(address) -> None:
    ipv6_definitions = test_json_schema["$defs"]["ipv6"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv6_definitions)


# Test the JSON schema with valid IPv4 CIDR addresses
@pytest.mark.parametrize("address", ["192.168.0.0/24", "10.0.0.0/8", "0.0.0.0/0", "172.0.0.1/32"])
def test_valid_ipv4_cidr_addresses(address) -> None:
    ipv4_cidr_definitions = test_json_schema["$defs"]["ipv4_cidr"]
    jsonschema.validate(address, ipv4_cidr_definitions)


# Test the JSON schema with some invalid IPv4 CIDR addresses, make sure they raise a ValidationError
@pytest.mark.parametrize("address", ["192.168.256.0/24", "10.0.0.0.0/8", "172.16.0.1/33", "8.8.8.8"])
def test_invalid_ipv4_cidr_addresses(address) -> None:
    ipv4_cidr_definitions = test_json_schema["$defs"]["ipv4_cidr"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv4_cidr_definitions)


# Test the JSON schema with valid IPv6 CIDR addresses
@pytest.mark.parametrize(
    "address",
    [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334/64",
        "2002:1::/48",
        "2001:db8::1/128",
        "2001:db8::/32",
    ],
)
def test_valid_ipv6_cidr_addresses(address) -> None:
    ipv6_cidr_definitions = test_json_schema["$defs"]["ipv6_cidr"]
    jsonschema.validate(address, ipv6_cidr_definitions)
    assert True


# Test the JSON schema with some invalid IPv6 CIDR addresses, make sure they raise a ValidationError
@pytest.mark.parametrize(
    "address",
    [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334/129",
        "2001:db8::1/0",
        "2001:db8::/20",
        "2001:db8::1/96",
    ],
)
def test_invalid_ipv6_cidr_addresses(address) -> None:
    ipv6_cidr_definitions = test_json_schema["$defs"]["ipv6_cidr"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv6_cidr_definitions)


# Test the JSON schema with valid IPv4 prefixes
prefixes = [f"/{i}" for i in range(33)]


@pytest.mark.parametrize("address", prefixes)
def test_valid_ipv4_prefixes(address) -> None:
    ipv4_prefix_definitions = test_json_schema["$defs"]["ipv4_prefix"]
    jsonschema.validate(address, ipv4_prefix_definitions)
    assert True


# Test the JSON schema with some invalid IPv4 prefixes, make sure they raise a ValidationError
@pytest.mark.parametrize("address", ["/33", "/-1", "/256", "/24.0"])
def test_invalid_ipv4_prefixes(address) -> None:
    ipv4_prefix_definitions = test_json_schema["$defs"]["ipv4_prefix"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv4_prefix_definitions)


# Test the JSON schema with valid IPv6 prefixes
prefixes = [f"/{i}" for i in range(32, 65, 4)]
prefixes.append("/128")


@pytest.mark.parametrize("address", prefixes)
def test_valid_ipv6_prefixes(address) -> None:
    ipv6_prefix_definitions = test_json_schema["$defs"]["ipv6_prefix"]
    jsonschema.validate(address, ipv6_prefix_definitions)
    assert True


# Test the JSON schema with some invalid IPv6 prefixes, make sure they raise a ValidationError
@pytest.mark.parametrize("address", ["/31", "/-1", "/256", "/24.0", "/127", "/55"])
def test_invalid_ipv6_prefixes(address) -> None:
    ipv6_prefix_definitions = test_json_schema["$defs"]["ipv6_prefix"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(address, ipv6_prefix_definitions)


# Test the JSON schema with valid domain names
@pytest.mark.parametrize("domain", ["example.com", "example.co.uk", "example.org", "example.net"])
def test_valid_domains(domain) -> None:
    domain_definitions = test_json_schema["$defs"]["domain"]
    jsonschema.validate(domain, domain_definitions)
    assert True


# Test the JSON schema with some invalid domain names, make sure they raise a ValidationError
@pytest.mark.parametrize(
    "domain",
    [
        "example",
        "example.",
        "example.c",
        "example.c.",
        "example.com.",
        ".example.com",
        "example.com..",
        "example.com.c",
        "example.com.c.",
    ],
)
def test_invalid_domains(domain) -> None:
    domain_definitions = test_json_schema["$defs"]["domain"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(domain, domain_definitions)
