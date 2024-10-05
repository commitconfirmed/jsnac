from jsnac.core.infer import SchemaInferer
import pytest

# Test SchemaInferer with jsnac_type: ipv4
def test_infer_ipv4() -> None:
    data = {"jsnac_type": "ipv4"}
    schema = SchemaInferer().infer_properties(data)
    assert schema == {"$ref": "#/$defs/ipv4"}