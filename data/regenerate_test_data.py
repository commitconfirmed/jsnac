#!/usr/bin/env python3
"""
Regenerate test data files for JSNAC by converting YAML files to JSON
and generating a JSON schema from a YAML file.

Functions:
    write_json(file: str) -> None:
        Converts a YAML file to a JSON file and writes the output to the same directory.
        Raises a ValueError if the YAML data is invalid.

    main() -> None:
        Main function that:
        - Determines the current file path.
        - Converts 'example.yml' and 'example-jsnac.yml' to JSON files.
        - Generates a JSON schema from 'example-jsnac.yml' and writes it to 'example.schema.json'.

Usage:
    Run this script when 'example.yml' or 'example-jsnac.yml' are updated to ensure
    that the test data files ('example-jsnac.json', 'example.json', and 'example.schema.json')
    are up-to-date with the latest data.
"""

import json
from pathlib import Path

import yaml

from jsnac.core.infer import SchemaInferer


def write_json(file: str) -> None:  # noqa: D103
    input_file = Path(file)
    output_file = input_file.with_suffix(".json")
    try:
        with input_file.open() as f:
            example_yaml_data = yaml.safe_load(f.read())
            f.close()
    except yaml.YAMLError as e:
        msg = "Invalid YAML data: %s", e
        raise ValueError(msg) from e
    example_json_data = json.dumps(example_yaml_data, indent=4)
    with output_file.open(mode="w") as f:
        f.write(example_json_data)
        f.close()


def main() -> None:  # noqa: D103
    # Get the current file path
    fp = Path(__file__).resolve().parent
    example_yaml_file = fp / "example.yml"
    example_jsnac_file = fp / "example-jsnac.yml"
    output_schema_file = fp / "example.schema.json"
    # Create JSON files for example.yml and example-jsnac.yml
    write_json(example_yaml_file)
    write_json(example_jsnac_file)
    # Generate a schema for example-jsnac.yml
    with example_jsnac_file.open() as f:
        jsnac = SchemaInferer()
        jsnac.add_yaml(f.read())
        schema = jsnac.build_schema()
        f.close()
    with output_schema_file.open(mode="w") as f:
        f.write(schema)
        f.close()


if __name__ == "__main__":
    main()
