#!/usr/bin/env python3
import json

import pytest

from jsnac.core.build import SchemaBuilder


# Test that bad JSON data raises an exception
def test_bad_json() -> None:
    data = "bad ^^^ json data {}"
    jsnac = SchemaBuilder()
    with pytest.raises(ValueError, match="Invalid JSON data:"):
        jsnac.add_json(data)


# Test that bad YAML data raises an exception
def test_bad_yaml() -> None:
    data = "value: bad ^^^ yaml data --: \n +2"
    jsnac = SchemaBuilder()
    with pytest.raises(ValueError, match="Invalid YAML data:"):
        jsnac.add_yaml(data)


# Test that no data raises an exception
def test_no_data() -> None:
    jsnac = SchemaBuilder()
    with pytest.raises(ValueError, match="No data has been added to the schema builder"):
        jsnac.build_schema()


# Test that custom headers can be set
def test_custom_headers() -> None:
    data = {
        "header": {
            "schema": "http://json-schema.org/draft/2020-12/schema",
            "title": "Test Title",
            "id": "test-schema.json",
            "description": "Test Description",
        }
    }
    jsnac = SchemaBuilder()
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["$schema"] == "http://json-schema.org/draft/2020-12/schema"
    assert schema["title"] == "Test Title"
    assert schema["$id"] == "test-schema.json"
    assert schema["description"] == "Test Description"


# Test that default headers are set
def test_default_headers() -> None:
    data = {"header": {}}
    jsnac = SchemaBuilder()
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["title"] == "JSNAC created Schema"
    assert schema["$id"] == "jsnac.schema.json"
    assert schema["description"] == "https://github.com/commitconfirmed/jsnac"
    assert schema["type"] == "object"
    assert schema["properties"] == {}


# Test that a custom js_kind of type pattern can be created
def test_custom_js_kind_pattern() -> None:
    data = {
        "js_kinds": {
            "test": {
                "title": "Test",
                "description": "Test Description",
                "type": "pattern",
                "regex": "^[0-9]{3}$",
            }
        }
    }
    jsnac = SchemaBuilder()
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["$defs"]["test"]["pattern"] == "^[0-9]{3}$"


# Test that our custom js_kind of pattern fails when regex is not provided
def test_custom_js_kind_pattern_fail() -> None:
    data = {
        "js_kinds": {
            "test": {
                "title": "Test",
                "description": "Test Description",
                "type": "pattern",
                "pattern": "wrong",
            }
        }
    }
    jsnac = SchemaBuilder()
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["$defs"]["test"]["type"] == "null"
    assert schema["$defs"]["test"]["title"] == "Error"
    assert schema["$defs"]["test"]["description"] == "No regex key provided"


# Test that an unknown js_kind type defaults to string
def test_custom_js_kind_unknown() -> None:
    data = {
        "js_kinds": {
            "test": {
                "title": "Test",
                "description": "Test Description",
                "type": "unknown",
            }
        }
    }
    jsnac = SchemaBuilder()
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["$defs"]["test"]["type"] == "string"
    assert schema["$defs"]["test"]["title"] == "Error"
    assert schema["$defs"]["test"]["description"] == "Invalid type (unknown), defaulted to string"


# Test all of our custom js_kind types
@pytest.mark.parametrize(
    "js_kind",
    [
        "ipv4",
        "ipv6",
        "ipv4_cidr",
        "ipv6_cidr",
        "ipv4_prefix",
        "ipv6_prefix",
        "domain",
        "email",
        "http_url",
        "uint16",
        "uint32",
        "uint64",
        "mtu",
        "mac",
        "mac_dot",
        "vlan",
        "docker_image",
    ],
)
def test_custom_js_kind_types(js_kind) -> None:
    jsnac = SchemaBuilder()
    data = {
        "schema": {
            "test_object": {
                "js_kind": {"name": js_kind},
            }
        }
    }
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["properties"]["test_object"]["$ref"] == f"#/$defs/{js_kind}"


# Test that general json schema types are generated correctly
@pytest.mark.parametrize(
    "js_kind",
    [
        "string",
        "number",
        "integer",
        "boolean",
        "null",
    ],
)
def test_default_schema_types(js_kind) -> None:
    jsnac = SchemaBuilder()
    data = {
        "schema": {
            "test_object": {
                "js_kind": {"name": js_kind},
            }
        }
    }
    jsnac.add_json(json.dumps(data))
    schema = json.loads(jsnac.build_schema())
    assert schema["properties"]["test_object"]["type"] == f"{js_kind}"
