import json
import os

import yaml

from jsnac.core.infer import SchemaInferer

# Use this when either example.yml or example-jsnac.yml are updated as a result of
# feature additions to JSNAC or other ongoing development to recreate
# the example-jsnac.json, example.json and example.schema.json files
# so we can ensure our tests are working with the latest data


# Load our test YAML, convert it to JSON, and write it to a file
def write_json(file: str) -> None:
    try:
        example_yaml_data = yaml.safe_load(open(file).read())
    except yaml.YAMLError as e:
        raise Exception(f"Invalid YAML data: {e}")
    example_json_data = json.dumps(example_yaml_data, indent=4)
    with open(file.replace(".yml", ".json"), "w") as f:
        f.write(example_json_data)


def main() -> None:
    # Get the current file path
    fp = os.path.dirname(os.path.abspath(__file__))
    example_yaml_file = os.path.join(fp, "example.yml")
    example_jsnac_file = os.path.join(fp, "example-jsnac.yml")
    output_schema_file = os.path.join(fp, "example.schema.json")
    # Create JSON files for example.yml and example-jsnac.yml
    write_json(example_yaml_file)
    write_json(example_jsnac_file)
    # Generate a schema for example-jsnac.yml
    jsnac = SchemaInferer()
    jsnac.add_yaml(open(example_jsnac_file).read())
    schema = jsnac.build()
    with open(output_schema_file, "w") as f:
        f.write(schema)


if __name__ == "__main__":
    main()
