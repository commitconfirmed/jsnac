#!/usr/bin/env python3
"""
File: jsnac/core/infer.py
Author: Andrew Jones
Copyright: 2024
License: Apache 2.0
Description: SchemaInferer class for inferring JSON schemas from JSON or YAML data.
"""

import json
import logging

import yaml


class SchemaInferer:
    """
    SchemaInferer is a class designed to infer JSON schemas from provided JSON or YAML data.

    Methods:
        __init__() -> None:
            Initializes the instance of the class, setting up a logger for the class instance.

        add_json(json_data: str) -> None:
            Parses the provided JSON data and stores it in the instance.

        add_yaml(yaml_data: str) -> None:
            Parses the provided YAML data, converts it to JSON format, and stores it in the instance.

        build() -> dict:
            Builds a JSON schema based on the data added to the schema inferer.

        infer_properties(data: dict) -> dict:
            Infers the JSON schema properties for the given data.

    """

    def __init__(self) -> None:
        """
        Initializes the instance of the class.

        This constructor sets up a logger for the class instance using the module's
        name. It also adds a NullHandler to the logger to prevent any logging
        errors if no other handlers are configured.

        Attributes:
            log (logging.Logger): Logger instance for the class.

        """
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

    # Take in JSON data and confirm it is valid JSON
    def add_json(self, json_data: str) -> None:
        """
        Parses the provided JSON data, and stores it in the instance.

        Args:
            json_data (str): A string containing JSON data.

        Raises:
            ValueError: If the provided JSON data is invalid.

        """
        try:
            load_json_data = json.loads(json_data)
            self.log.debug("JSON content: \n %s", json.dumps(load_json_data, indent=4))
            self.data = load_json_data
        except json.JSONDecodeError as e:
            msg = "Invalid JSON data: %s", e
            self.log.exception(msg)
            raise ValueError(msg) from e

    def add_yaml(self, yaml_data: str) -> None:
        """
        Parses the provided YAML data, converts it to JSON format, and stores it in the instance.

        Args:
            yaml_data (str): A string containing YAML formatted data.

        Raises:
            ValueError: If the provided YAML data is invalid.

        """
        try:
            load_yaml_data = yaml.safe_load(yaml_data)
            self.log.debug("YAML content: \n %s", load_yaml_data)
        except yaml.YAMLError as e:
            msg = "Invalid YAML data: %s", e
            self.log.exception(msg)
            raise ValueError(msg) from e
        json_dump = json.dumps(load_yaml_data, indent=4)
        json_data = json.loads(json_dump)
        self.log.debug("JSON content: \n %s", json_dump)
        self.data = json_data

    def build(self) -> str:
        """
        Builds a JSON schema based on the data added to the schema inferer.

        This methos builds the base schema including our custom definitions for common data types.
        Properties are handled by the infer_properties method to infer the properties of the schema
        based on the input data provided.

        Returns:
            str: A JSON string representing the constructed schema.

        Raises:
            ValueError: If no data has been added to the schema inferer.

        """
        # Check if the data has been added
        if not hasattr(self, "data"):
            msg = "No data has been added to the schema inferer. Use add_json or add_yaml to add data."
            self.log.error(msg)
            raise ValueError(msg)
        data = self.data

        self.log.debug("Building schema for: \n %s ", json.dumps(data, indent=4))
        # Using draft-07 until vscode $dynamicRef support is added (https://github.com/microsoft/vscode/issues/155379)
        # Feel free to replace this with http://json-schema.org/draft/2020-12/schema if not using vscode.
        # I want to fix this with a flag to the CLI to allow you to choose the draft version you want to use
        # in the future (or insert your own).
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "title": "JSNAC Created Schema",
            "description": "The below schema was created by JSNAC (https://github.com/commitconfirmed/jsnac)",
            "$defs": {
                "ipv4": {
                    "type": "string",
                    "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])$",  # noqa: E501
                    "title": "IPv4 Address",
                    "description": "IPv4 address (String) \n Format: xxx.xxx.xxx.xxx",
                },
                # Decided to just go simple for now, may add more complex validation in the future from
                # https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
                "ipv6": {
                    "type": "string",
                    "pattern": "^(([a-fA-F0-9]{1,4}|):){1,7}([a-fA-F0-9]{1,4}|:)$",
                    "title": "IPv6 Address",
                    "description": "Short IPv6 address (String) \n Accepts both full and short form addresses, link-local addresses, and IPv4-mapped addresses",  # noqa: E501
                },
                "ipv4_cidr": {
                    "type": "string",
                    "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",  # noqa: E501
                    "title": "IPv4 CIDR",
                    "description": "IPv4 CIDR (String) \n Format: xxx.xxx.xxx.xxx/xx",
                },
                "ipv6_cidr": {
                    "type": "string",
                    "pattern": "(([a-fA-F0-9]{1,4}|):){1,7}([a-fA-F0-9]{1,4}|:)/(32|36|40|44|48|52|56|60|64|128)$",
                    "title": "IPv6 CIDR",
                    "description": "Full IPv6 CIDR (String) \n Format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx",
                },
                "ipv4_prefix": {
                    "type": "string",
                    "title": "IPv4 Prefix",
                    "pattern": "^/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",
                    "description": "IPv4 Prefix (String) \n Format: /xx between 0 and 32",
                },
                "ipv6_prefix": {
                    "type": "string",
                    "title": "IPv6 Prefix",
                    "pattern": "^/(32|36|40|44|48|52|56|60|64|128)$",
                    "description": "IPv6 prefix (String) \n Format: /xx between 32 and 64 in increments of 4. also /128",  # noqa: E501
                },
                "domain": {
                    "type": "string",
                    "pattern": "^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$",
                    "title": "Domain Name",
                    "description": "Domain name (String) \n Format: example.com",
                },
                # String is a default type, but in this instance we restict it to
                # alphanumeric + special characters with a max length of 255.
                "string": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9!@#$%^&*()_+-\\{\\}|:;\"'<>,.?/ ]{1,255}$",
                    "title": "String",
                    "description": "Alphanumeric string with special characters (String) \n Max length: 255",
                },
            },
            "type": "object",
            "additionalProperties": False,
            "properties": self.infer_properties(data)["properties"],
        }
        return json.dumps(schema, indent=4)

    def infer_properties(self, data: str) -> dict:  # noqa: C901 PLR0912 PLR0915 (To be fixed)
        """
        Infers the JSON schema properties for the given data.

        This method analyzes the input data and generates a corresponding JSON schema.
        It supports custom schema definitions based on the "jsnac_type" key in the input dictionary.

        Args:
            data (str): The input data to infer the schema from.

        Returns:
            dict: A dictionary representing the inferred JSON schema.

        Schema Inference rules (based on the input data type):
            - Is a dictionary and contains the "jsnac_type" key, the method uses custom schema definitions
            - Is a dictionary without the "jsnac_type" key, we infer the schema recursively for each key-value pair.
            - Is a list, the method infers the schema for the first item in the list.
            - Is a string, integer, float, or boolean, the method infers the corresponding JSON schema type.
            - Is Of an unrecognized type, the method defaults to a null schema.

        """
        schema = {}
        # Check if the dictionary has a jsnac_type key in it, then we know we can use our custom schema definitions
        if isinstance(data, dict):
            if "jsnac_type" in data:  # Split this out into a separate method to be ruff compliant
                match data["jsnac_type"]:
                    case "ipv4":
                        schema["$ref"] = "#/$defs/ipv4"
                    case "ipv6":
                        schema["$ref"] = "#/$defs/ipv6"
                    case "ipv4_cidr":
                        schema["$ref"] = "#/$defs/ipv4_cidr"
                    case "ipv6_cidr":
                        schema["$ref"] = "#/$defs/ipv6_cidr"
                    case "ipv4_prefix":
                        schema["$ref"] = "#/$defs/ipv4_prefix"
                    case "ipv6_prefix":
                        schema["$ref"] = "#/$defs/ipv6_prefix"
                    case "domain":
                        schema["$ref"] = "#/$defs/domain"
                    case "string":
                        schema["$ref"] = "#/$defs/string"
                    case "pattern":
                        if "jsnac_pattern" not in data:
                            self.log.error("jsnac_pattern key is required for jsnac_type: pattern.")
                            schema["type"] = "null"
                            schema["title"] = "Error"
                            schema["description"] = "No jsnac_pattern key provided"
                        else:
                            schema["type"] = "string"
                            schema["pattern"] = data["jsnac_pattern"]
                            schema["title"] = "Custom Pattern"
                            schema["description"] = "Custom Pattern (regex) \n Pattern: " + data["jsnac_pattern"]
                    case "choice":
                        if "jsnac_choices" not in data:
                            self.log.error("jsnac_choices key is required for jsnac_type: choice.")
                            schema["enum"] = "Error"
                            schema["title"] = "Error"
                            schema["description"] = "No jsnac_choices key provided"
                        else:
                            schema["enum"] = data["jsnac_choices"]
                            schema["title"] = "Custom Choice"
                            schema["description"] = "Custom Choice (enum) \n Choices: " + ", ".join(
                                data["jsnac_choices"]
                            )
                    case _:
                        self.log.error("Invalid jsnac_type: (%s), defaulting to null", data["jsnac_type"])
                        schema["type"] = "null"
                        schema["title"] = "Error"
                        schema["description"] = "Invalid jsnac_type (" + data["jsnac_type"] + ") defined"
            # If not, simply continue inferring the schema
            else:
                schema["type"] = "object"
                schema["properties"] = {k: self.infer_properties(v) for k, v in data.items()}

        elif isinstance(data, list):
            if len(data) > 0:
                schema["type"] = "array"
                schema["items"] = self.infer_properties(data[0])
            else:
                schema["type"] = "array"
                schema["items"] = {}
        elif isinstance(data, str):
            schema["type"] = "string"
        elif isinstance(data, int):
            schema["type"] = "integer"
        elif isinstance(data, float):
            schema["type"] = "number"
        elif isinstance(data, bool):
            schema["type"] = "boolean"
        else:
            schema["type"] = "null"
        return schema
