from jsnac.core.infer import SchemaInferer
import json
import yaml

# Use this when either example.yml or example-jsnac.yml are updated as a result of
# feature additions to JSNAC or other ongoing development to recreate
# the example-jsnac.json, example.json and example.schema.json files 
# so we can ensure our tests are working with the latest data

# Load our test YAML, convert it to JSON, and write it to a file
def write_json(file: str) -> None:
    try:
        test_yaml_data = yaml.safe_load(open(file).read())
    except yaml.YAMLError as e:
        raise Exception(f"Invalid YAML data: {e}")
    test_json_data = json.dumps(test_yaml_data, indent=4)
    with open(file.replace('.yml', '.json'), 'w') as f:
        f.write(test_json_data)

def main() -> None:
    # Create JSON files for example.yml and example-jsnac.yml
    write_json('example.yml')
    write_json('example-jsnac.yml')
    # Generate a schema for example-jsnac.yml
    jsnac = SchemaInferer()
    jsnac.add_yaml(open('example-jsnac.yml').read())
    schema = jsnac.build()
    with open('example.schema.json', 'w') as f:
        f.write(schema)

if __name__ == "__main__":
    main()