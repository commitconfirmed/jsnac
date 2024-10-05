import json
import yaml
import jsonschema
import pytest

# Load our test YAML and convert it to JSON
try:
    test_yaml_data = yaml.safe_load(open('data/test.yml').read())
except yaml.YAMLError as e:
    raise Exception(f"Invalid YAML data: {e}")
test_json_dump = json.dumps(test_yaml_data, indent=4)
test_json_data = json.loads(test_json_dump)
test_json_schema = json.loads(open('data/test.schema.json').read())

def test_all() -> None:
    jsonschema.validate(test_json_data, test_json_schema)