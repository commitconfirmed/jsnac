#!/usr/bin/env python3
import json

from jsnac.core.build import SchemaBuilder


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
