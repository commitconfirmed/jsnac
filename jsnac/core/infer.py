#!/usr/bin/env python3

import json
import logging
from typing import ClassVar

import yaml


class SchemaInferer:
    """
    SchemaInferer is a class that infers JSON schemas from provided JSON or YAML data.

        user_defined_kinds (dict): A class variable that stores user-defined kinds.

    Methods:
        __init__():
            Initializes the instance of the class, setting up a logger.

        _view_user_defined_kinds() -> dict:
            Returns the user-defined kinds currently stored in the class variable.

        _add_user_defined_kinds(kinds: dict) -> None:
            Adds user-defined kinds to the class variable.

        add_json(json_data: str) -> None:
            Parses the provided JSON data and stores it in the instance.

        add_yaml(yaml_data: str) -> None:
            Parses the provided YAML data, converts it to JSON format, and stores it in the instance.

        build_schema() -> str:
            Builds a JSON schema based on the data added to the schema inferer. Returns the constructed schema.

        _build_definitions(data: dict) -> dict:
            Builds the definitions section of the JSON schema.

        _build_properties(data: dict) -> dict:
            Builds the properties section of the JSON schema.

        _build_property(obj: str, obj_data: dict) -> dict:
            Builds a property for the JSON schema.

        _build_property_type(obj: str, obj_data: dict) -> dict:
            Builds the type for a property in the JSON schema.

        _build_array_items(obj: str, obj_data: dict) -> dict:
            Builds the items for an array property in the JSON schema.

        _build_kinds(obj: str, data: dict) -> dict:
            Builds the kinds for a property in the JSON schema.

    """

    user_defined_kinds: ClassVar[dict] = {}

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
    def _view_user_defined_kinds(cls) -> dict:
        return cls.user_defined_kinds

    @classmethod
    def _add_user_defined_kinds(cls, kinds: dict) -> None:
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
            self.log.debug("JSON content: \n%s", json.dumps(load_json_data, indent=4))
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
            self.log.debug("YAML content: \n%s", load_yaml_data)
        except yaml.YAMLError as e:
            msg = "Invalid YAML data: %s", e
            self.log.exception(msg)
            raise ValueError(msg) from e
        json_dump = json.dumps(load_yaml_data, indent=4)
        json_data = json.loads(json_dump)
        self.log.debug("JSON content: \n%s", json_dump)
        self.data = json_data

    def build_schema(self) -> str:
        """
        Builds a JSON schema based on the data added to the schema inferer.
        This method constructs a JSON schema using the data previously added via
        `add_json` or `add_yaml` methods. It supports JSON Schema draft-07 by default,
        but can be configured to use other drafts if needed.

        Returns:
            str: A JSON string representing the constructed schema.

        Raises:
            ValueError: If no data has been added to the schema inferer.

        Notes:
            - The schema's metadata (e.g., $schema, title, $id, description) is derived
              from the "header" section of the provided data.
            - Additional sub-schemas (definitions) can be added via the "kinds" section
              of the provided data.
            - The schemas for individual and nested properties are constructed
              based on the "schema" section of the provided data.

        """
        # Check if the data has been added
        if not hasattr(self, "data"):
            msg = "No data has been added to the schema inferer. Use add_json or add_yaml to add data."
            self.log.error(msg)
            raise ValueError(msg)
        data = self.data

        self.log.debug("Building schema for: \n%s ", json.dumps(data, indent=4))
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
        """
        Build a dictionary of definitions based on predefined types and additional kinds provided in the input data.

        Args:
            data (dict): A dictionary containing additional kinds to be added to the definitions.

        Returns:
            dict: A dictionary containing definitions for our predefined types such as 'ipv4', 'ipv6', etc.
                  Additional kinds from the input data are also included.

        Raises:
            None

        """
        self.log.debug("Building definitions for: \n%s ", json.dumps(data, indent=4))
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
        }
        # Check passed data for additional kinds and add them to the definitions
        for kind, kind_data in data.items():
            self.log.debug("Building custom kind (%s): \n%s ", kind, json.dumps(kind_data, indent=4))
            definitions[kind] = {}
            definitions[kind]["title"] = kind_data.get("title", f"{kind}")
            definitions[kind]["description"] = kind_data.get("description", f"Custom Kind: {kind}")
            # Only support a custom kind of pattern for now, will add more in the future
            match kind_data.get("type"):
                case "pattern":
                    definitions[kind]["type"] = "string"
                    if "regex" in kind_data:
                        definitions[kind]["pattern"] = kind_data["regex"]
                        self._add_user_defined_kinds({kind: True})
                    else:
                        self.log.error("regex key is required for kind (%s) with type pattern", kind)
                        definitions[kind]["type"] = "null"
                        definitions[kind]["title"] = "Error"
                        definitions[kind]["description"] = "No regex key provided"
                case _:
                    self.log.error("Invalid type (%s) for kind (%s), defaulting to string", kind_data.get("type"), kind)
                    definitions[kind]["type"] = "string"
        self.log.debug("Returned Definitions: \n%s ", json.dumps(definitions, indent=4))
        return definitions

    def _build_properties(self, data: dict) -> dict:
        self.log.debug("Building properties for: \n%s ", json.dumps(data, indent=4))
        properties: dict = {}
        stack = [(properties, data)]

        while stack:
            current_properties, current_data = stack.pop()
            for obj, obj_data in current_data.items():
                self.log.debug("Object: %s ", obj)
                self.log.debug("Object Data: %s ", obj_data)
                # Build the property for the object
                current_properties[obj] = self._build_property(obj, obj_data)
                # Check if there is a nested object or array type and add it to the stack
                if "type" in obj_data and obj_data["type"] == "object" and "properties" in obj_data:
                    stack.append((current_properties[obj]["properties"], obj_data["properties"]))
                elif "type" in obj_data and obj_data["type"] == "array" and "items" in obj_data:
                    item_data = obj_data["items"]
                    # Array is nested if it contains properties
                    if "properties" in item_data:
                        stack.append((current_properties[obj]["items"]["properties"], item_data["properties"]))

        self.log.debug("Returned Properties: \n%s ", json.dumps(properties, indent=4))
        return properties

    def _build_property(self, obj: str, obj_data: dict) -> dict:
        self.log.debug("Building property for Object (%s): \n%s ", obj, json.dumps(obj_data, indent=4))
        property_dict: dict = {}

        if "title" in obj_data:
            property_dict["title"] = obj_data["title"]
        if "description" in obj_data:
            property_dict["description"] = obj_data["description"]
        if "type" in obj_data:
            property_dict.update(self._build_property_type(obj, obj_data))
        elif "kind" in obj_data:
            property_dict.update(self._build_kinds(obj, obj_data["kind"]))

        if "required" in obj_data:
            property_dict["required"] = obj_data["required"]

        self.log.debug("Returned Property: \n%s ", json.dumps(property_dict, indent=4))
        return property_dict

    def _build_property_type(self, obj: str, obj_data: dict) -> dict:
        self.log.debug("Building property type for Object (%s): \n%s ", obj, json.dumps(obj_data, indent=4))
        property_type = {"type": obj_data["type"]}
        match obj_data["type"]:
            case "object":
                property_type["properties"] = {}
            case "array":
                property_type.update(self._build_array_items(obj, obj_data))
            case _:
                self.log.error("Invalid type (%s), defaulting to Null", obj_data["type"])
                property_type["type"] = "null"
        self.log.debug("Returned Property Type: \n%s ", json.dumps(property_type, indent=4))
        return property_type

    def _build_array_items(self, obj: str, obj_data: dict) -> dict:
        self.log.debug("Building array items for Object (%s): \n%s ", obj, json.dumps(obj_data, indent=4))
        array_items = {}
        if "items" in obj_data:
            item_data = obj_data["items"]
            if "type" in item_data:
                array_items["items"] = {"type": item_data["type"]}
                if "properties" in item_data:
                    array_items["items"]["properties"] = {}
                if "required" in item_data:
                    array_items["items"]["required"] = item_data["required"]
            elif "kind" in item_data:
                array_items["items"] = self._build_kinds(obj, item_data["kind"])
            else:
                self.log.error("Array items require a type or kind key")
                array_items["items"] = {"type": "null"}
        else:
            self.log.error("Array type requires an items key")
            array_items["items"] = {"type": "null"}
        self.log.debug("Returned Array Items: \n%s ", json.dumps(array_items, indent=4))
        return array_items

    def _build_kinds(self, obj: str, data: dict) -> dict:  # noqa: C901 PLR0912
        self.log.debug("Building kinds for Object (%s): \n%s ", obj, json.dumps(data, indent=4))
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
            # For the choice kind, read the choices object
            case "choice":
                if "choices" in data:
                    kind["enum"] = data["choices"]
                else:
                    self.log.error("Choice kind requires a choices object")
                    kind["description"] = "Choice kind requires a choices object"
                    kind["type"] = "null"
            # Default types
            case "string":
                kind["type"] = "string"
                kind["title"] = obj
                kind["description"] = "String"
            case "number":
                kind["type"] = "number"
                kind["description"] = "Integer or Float"
            case "boolean":
                kind["type"] = "boolean"
                kind["description"] = "Boolean"
            case "null":
                kind["type"] = "null"
                kind["description"] = "Null"
            case _:
                # Check if the kind is a user defined kind
                if data.get("name") in self._view_user_defined_kinds():
                    kind["$ref"] = "#/$defs/{}".format(data["name"])
                else:
                    self.log.error("Invalid kind (%s), defaulting to Null", data)
                    kind["description"] = f"Invalid kind ({data}), defaulting to Null"
                    kind["type"] = "null"
        return kind
