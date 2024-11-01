#!/usr/bin/env python3
from jsnac.core.infer import SchemaInferer


# Test SchemaInferer with jsnac_type: ipv4
def test_infer_ipv4() -> None:
    data = {"jsnac_type": "ipv4"}
    schema = SchemaInferer().infer_properties(data)
    assert schema == {"$ref": "#/$defs/ipv4"}


# Test SchemaInferer with jsnac_type: ipv6
def test_infer_ipv6() -> None:
    data = {"jsnac_type": "ipv6"}
    schema = SchemaInferer().infer_properties(data)
    assert schema == {"$ref": "#/$defs/ipv6"}


# Test SchemaInferer with jsnac_type: ipv4_cidr
def test_infer_ipv4_cidr() -> None:
    data = {"jsnac_type": "ipv4_cidr"}
    schema = SchemaInferer().infer_properties(data)
    assert schema == {"$ref": "#/$defs/ipv4_cidr"}


# Test SchemaInferer with an invalid jsnac_type
def test_infer_invalid_type() -> None:
    data = {"jsnac_type": "invalid"}
    schema = SchemaInferer().infer_properties(data)
    assert schema == {
        "type": "null",
        "title": "Error",
        "description": "Invalid jsnac_type (invalid) defined",
    }
