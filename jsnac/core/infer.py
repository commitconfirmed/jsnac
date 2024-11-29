#!/usr/bin/env python3

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

    user_defined_kinds: dict = {}

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

    @classmethod
    def access_user_defined_kinds(cls) -> dict:
        return cls.user_defined_kinds

    @classmethod
    def add_user_defined_kinds(cls, kinds: dict) -> None:
        cls.user_defined_kinds.update(kinds)

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

    def build_schema(self) -> str:
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
        schema = {
            "$schema": data.get("header", {}).get("schema", "http://json-schema.org/draft-07/schema#"),
            "title": data.get("header", {}).get("title", "JSNAC created Schema"),
            "$id": data.get("header", {}).get("id", "jsnac.schema.json"),
            "description": data.get("header", {}).get("description", "https://github.com/commitconfirmed/jsnac"),
            "$defs": self._build_definitions(data.get("kinds", {})),
            "type": data.get("type", "object"),
            "additionalProperties": data.get("additionalProperties", False),
            "properties": self._build_properties(data.get("schema", {})),
        }
        return json.dumps(schema, indent=4)

    def _build_definitions(self, data: dict) -> dict:
        self.log.debug("Building definitions for: \n %s ", json.dumps(data, indent=4))
        definitions = {
            # JSNAC defined data types
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
                "description": "IPv6 prefix (String) \n Format: /xx between 32 and 64 in increments of 4. also /128",
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
        }
        # Check passed data for additional kinds and add them to the definitions
        for kind, kind_data in data.items():
            self.log.debug("Kind: %s ", kind)
            self.log.debug("Kind Data: %s ", kind_data)
            # Add the kind to the definitions
            definitions[kind] = {}
            definitions[kind]["title"] = kind_data.get("title", "%s" % kind)
            definitions[kind]["description"] = kind_data.get("description", "Custom Kind: %s" % kind)
            # Only support a custom kind of pattern for now, will add more in the future
            match kind_data.get("type"):
                case "pattern":
                    definitions[kind]["type"] = "string"
                    if "regex" in kind_data:
                        definitions[kind]["pattern"] = kind_data["regex"]
                        self.add_user_defined_kinds({kind: True})
                    else:
                        self.log.error("regex key is required for kind (%s) with type pattern", kind)
                        definitions[kind]["type"] = "null"
                        definitions[kind]["title"] = "Error"
                        definitions[kind]["description"] = "No regex key provided"
                case _:
                    self.log.error("Invalid type (%s) for kind (%s), defaulting to string", kind_data.get("type"), kind)
                    definitions[kind]["type"] = "string"
        self.log.debug("Returned Definitions: \n %s ", json.dumps(definitions, indent=4))
        return definitions

    def _build_properties(self, data: dict) -> dict:
        self.log.debug("Building properties for: \n %s ", json.dumps(data, indent=4))
        properties: dict = {}
        for object, object_data in data.items():
            self.log.debug("Object: %s ", object)
            self.log.debug("Object Data: %s ", object_data)
            # Think of a way to have better defaults for title and description
            # Also, inner properties aren't getting a default description for some reason?
            properties[object] = {}
            properties[object]["title"] = object_data.get("title", "%s" % object)
            properties[object]["description"] = object_data.get("description", "Object: %s" % object)
            # Check if our object has a type, if so we will continue to dig depper until kinds are found
            if "type" in object_data:
                match object_data.get("type"):
                    case "object":
                        properties[object]["type"] = "object"
                        if "properties" in object_data:
                            properties[object]["properties"] = self._build_properties(object_data["properties"])
                    case "array":
                        properties[object]["type"] = "array"
                        # Check if the array contains an object type, if so we will build the properties for it
                        if "type" in object_data["items"]:
                            properties[object]["items"] = {}
                            properties[object]["items"]["type"] = object_data["items"]["type"]
                            properties[object]["items"]["properties"] = self._build_properties(
                                object_data["items"]["properties"]
                            )
                        # Otherwise its just a list of a specific kind
                        elif "kind" in object_data["items"]:
                            properties[object]["items"] = self._build_kinds(object_data["items"]["kind"])
                    case _:
                        self.log.error(
                            "Invalid type (%s) for object (%s), defaulting to Null", object_data.get("type"), object
                        )
                        properties[object]["type"] = "null"
            # We've reached an object with a kind key, we can now build the reference based on the kind
            elif "kind" in object_data:
                kind = self._build_kinds(object_data["kind"])
                properties[object] = kind
        self.log.debug("Returned Properties: \n %s ", json.dumps(properties, indent=4))
        return properties

    def _build_kinds(self, data: dict) -> dict:  # noqa: C901 PLR0912
        self.log.debug("Building kinds for: \n %s ", json.dumps(data, indent=4))
        kind: dict = {}
        # Check if the kind has a type, if so we will continue to dig depper until kinds are found
        # I should update this to be ruff compliant, but it makes sense to me at the moment
        match data.get("name"):
            # Kinds with regex patterns
            case "ipv4":
                kind["$ref"] = "#/$defs/ipv4"
            case "ipv6":
                kind["$ref"] = "#/$defs/ipv6"
            case "ipv4_cidr":
                kind["$ref"] = "#/$defs/ipv4_cidr"
            case "ipv6_cidr":
                kind["$ref"] = "#/$defs/ipv6_cidr"
            case "ipv4_prefix":
                kind["$ref"] = "#/$defs/ipv4_prefix"
            case "ipv6_prefix":
                kind["$ref"] = "#/$defs/ipv6_prefix"
            case "domain":
                kind["$ref"] = "#/$defs/domain"
            # For the choice kind, read the choices key
            case "choice":
                if "choices" in data:
                    kind["enum"] = data["choices"]
                else:
                    self.log.error("Choice kind requires a choices key")
                    kind["type"] = "null"
            # Default types
            case "string":
                kind["type"] = "string"
            case "number":
                kind["type"] = "number"
            case "boolean":
                kind["type"] = "boolean"
            case "null":
                kind["type"] = "null"
            case _:
                # Check if the kind is a user defined kind
                if data.get("name") in self.access_user_defined_kinds():
                    kind["$ref"] = "#/$defs/{}".format(data["name"])
                else:
                    self.log.error("Invalid kind (%s), defaulting to Null", data)
                    kind["type"] = "null"
        return kind
