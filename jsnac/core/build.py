#!/usr/bin/env python3

import json
import logging
from typing import Any, ClassVar

import yaml


class SchemaBuilder:
    """
    SchemaBuilder is a class designed to build JSON schemas from JSON or YAML data.
    It supports predefined types and allows for user-defined kinds.

    Variables:
        user_defined_kinds (dict): A class variable to store user-defined kinds.

    Methods:
        __init__():
            Initializes the instance of the class, setting up a logger.
        _view_user_defined_kinds() -> dict:
            Class method to view any user-defined kinds.
        _add_user_defined_kinds(kinds: dict) -> None:
            Class method to add a user-defined kind.
        add_json(json_data: str) -> None:
            Parses the provided JSON data and stores it in the instance.
        add_yaml(yaml_data: str) -> None:
            Parses the provided YAML data, converts it to JSON format, and stores it in the instance.
        build_schema() -> str:
            The main function of this class, returns a JSON schema based on the data added to the schema builder.
        _build_definitions(data: dict) -> dict:
            Builds a dictionary of definitions based on predefined types and any additional js_kinds provided.
        _build_properties(title: str, data: dict) -> dict:
            Builds properties for the schema based on the provided data.
        _build_kinds(title: str, data: dict) -> dict:
            Builds js_kinds for the schema based on the provided data.

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
            self.log.debug("JSON content: \n%s", load_json_data)
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
        Builds a JSON schema based on the data added to the schema builder.
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
            - Additional sub-schemas (definitions) can be added via the "js_kinds" section
              of the provided data.
            - The schemas for individual and nested properties are constructed
              based on the "schema" section of the provided data.

        """
        # Check if the data has been added
        if not hasattr(self, "data"):
            msg = "No data has been added to the schema builder. Use add_json or add_yaml to add data."
            self.log.error(msg)
            raise ValueError(msg)
        data = self.data

        self.log.debug("Building schema for: \n%s ", data)
        # Using draft-07 until vscode $dynamicRef support is added (https://github.com/microsoft/vscode/issues/155379)
        # Feel free to replace this with http://json-schema.org/draft/2020-12/schema if not using vscode.
        schema = {
            "$schema": data.get("header", {}).get("schema", "http://json-schema.org/draft-07/schema#"),
            "title": data.get("header", {}).get("title", "JSNAC created Schema"),
            "$id": data.get("header", {}).get("id", "jsnac.schema.json"),
            "description": data.get("header", {}).get("description", "https://github.com/commitconfirmed/jsnac"),
            "$defs": self._build_definitions(data.get("js_kinds", {})),
            "type": data.get("type", "object"),
            "additionalProperties": data.get("additionalProperties", False),
            "properties": self._build_properties("Default", data.get("schema", {})),
        }
        return json.dumps(schema, indent=4)

    def _build_definitions(self, data: dict) -> dict:
        """
        Build a dictionary of definitions based on predefined types and additional js_kinds provided in the input data.

        Args:
            data (dict): A dictionary containing additional js_kinds to be added to the definitions.

        Returns:
            dict: A dictionary containing definitions for our predefined types such as 'ipv4', 'ipv6', etc.
                  Additional js_kinds from the input data are also included.

        Raises:
            None

        """
        self.log.debug("Building definitions for: \n%s ", data)
        definitions: dict[str, dict[str, Any]] = {
            # JSNAC defined data types, may eventually move these to a separate file
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
                "description": "Short IPv6 address (String) \nAccepts both full and short form addresses, link-local addresses, and IPv4-mapped addresses",  # noqa: E501
            },
            "ipv4_cidr": {
                "type": "string",
                "pattern": "^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",  # noqa: E501
                "title": "IPv4 CIDR",
                "description": "IPv4 CIDR (String) \nFormat: xxx.xxx.xxx.xxx/xx",
            },
            "ipv6_cidr": {
                "type": "string",
                "pattern": "^(([a-fA-F0-9]{1,4}|):){1,7}([a-fA-F0-9]{1,4}|:)/(32|36|40|44|48|52|56|60|64|128)$",
                "description": "Full IPv6 CIDR (String) \nFormat: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx",
            },
            "ipv4_prefix": {
                "type": "string",
                "pattern": "^/(1[0-9]|[0-9]|2[0-9]|3[0-2])$",
                "description": "IPv4 Prefix (String) \nFormat: /xx between 0 and 32",
            },
            "ipv6_prefix": {
                "type": "string",
                "pattern": "^/(32|36|40|44|48|52|56|60|64|128)$",
                "description": "IPv6 prefix (String) \nFormat: /xx between 32 and 64 in increments of 4. also /128",
            },
            "domain": {
                "type": "string",
                "pattern": "^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$",
                "description": "Domain name (String) \nFormat: example.com",
            },
            "email": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                "description": "Email address (String) \nFormat: user@domain.com",
            },
            "http_url": {
                "type": "string",
                "pattern": "^(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})([/\\w .-]*)*\\??([^#\\s]*)?(#.*)?$",
                "description": "HTTP(s) URL (String) \nFormat: http://example.com",
            },
            "uint16": {
                "type": "integer",
                "minimum": 0,
                "maximum": 65535,
                "description": "16-bit Unsigned Integer \nRange: 0 to 65535",
            },
            "uint32": {
                "type": "integer",
                "minimum": 0,
                "maximum": 4294967295,
                "description": "32-bit Unsigned Integer \nRange: 0 to 4294967295",
            },
            "uint64": {
                "type": "integer",
                "minimum": 0,
                "maximum": 18446744073709551615,
                "description": "64-bit Unsigned Integer \nRange: 0 to 18446744073709551615",
            },
            "mtu": {
                "type": "integer",
                "minimum": 68,
                "maximum": 9192,
                "description": "Maximum Transmission Unit (MTU) \nRange: 68 to 9192",
            },
            "mac": {
                "type": "string",
                "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                "description": "MAC Address (String) \nFormat: xx:xx:xx:xx:xx:xx",
            },
            "mac_dot": {
                "type": "string",
                "pattern": "^([0-9A-Fa-f]{4}[.]){2}([0-9A-Fa-f]{4})$",
                "description": "MAC Address with dots (String) \nFormat: xxxx.xxxx.xxxx",
            },
            "vlan": {
                "type": "integer",
                "minimum": 1,
                "maximum": 4094,
                "description": "VLAN ID (Integer) \nRange: 1 to 4094",
            },
            "docker_image": {
                "type": "string",
                "pattern": "^[a-z0-9]+(?:[._-][a-z0-9]+)*$",
                "description": "Docker Image Name (String) \nFormat: alpine:latest",
            },
        }
        # Check passed data for additional js_kinds and add them to the definitions
        for kind, kind_data in data.items():
            self.log.debug("Building custom js_kind (%s): \n%s ", kind, kind_data)
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
                        self.log.error("regex key is required for js_kind (%s) with type pattern", kind)
                        definitions[kind]["type"] = "null"
                        definitions[kind]["title"] = "Error"
                        definitions[kind]["description"] = "No regex key provided"
                case _:
                    self.log.error(
                        "Invalid type (%s) for js_kind (%s), defaulting to string", kind_data.get("type"), kind
                    )
                    definitions[kind]["type"] = "string"
                    definitions[kind]["title"] = "Error"
                    definitions[kind]["description"] = f"Invalid type ({kind_data.get('type')}), defaulted to string"
        self.log.debug("Returned Definitions: \n%s ", data)
        return definitions

    def _build_properties(self, title: str, data: dict) -> dict:
        """
        Recursively builds properties for a given title and data dictionary.

        Args:
            title (str): The title for the properties being built.
            data (dict): The data dictionary containing properties to be processed.

        Returns:
            dict: A dictionary representing the built properties.

        The function processes the input data dictionary to build properties based on its structure.
        If the data contains a "js_kind" key, it delegates to the _build_kinds method.
        If the data contains nested dictionaries or lists, it recursively processes them.
        We also type to "object" or "array" based on the presence of "properties" or "items" keys.

        """
        self.log.debug("Building properties for: \n%s ", data)
        # Check if there is a nested dictionary, if so we will check all keys and valid and then depending
        # on the key we will recursively call this function again or build our js_kinds
        if isinstance(data, dict):
            if "js_kind" in data:
                return self._build_kinds(title, data["js_kind"])
            # Else
            properties = {}
            # Add the type depending if our YAML has a properties or items key
            if "properties" in data:
                properties["type"] = "object"
                # Check for additional properties, otherwise set to false
                properties["additionalProperties"] = data.get("additional_properties", False)
            if "items" in data:
                properties["type"] = "array"
            properties.update({k: self._build_properties(k, v) for k, v in data.items()})
            return properties
        if isinstance(data, list):
            return [self._build_properties(title, item) for item in data]
        return data

    def _build_kinds(self, title: str, data: dict) -> dict:  # noqa: PLR0912
        """
        Builds js_kinds for a given title and data dictionary.

        Args:
            title (str): The title for the js_kinds being built.
            data (dict): The data dictionary containing js_kinds to be processed.

        Returns:
            dict: A dictionary representing the built js_kinds.

        """
        self.log.debug("Building js_kinds for Object (%s): \n%s ", title, data)
        kind: dict = {}
        # Add the title passed in from the parent object
        kind["title"] = title
        valid_js_kinds = [
            "ipv4",
            "ipv6",
            "ipv4_cidr",
            "ipv6_cidr",
            "ipv4_prefix",
            "ipv6_prefix",
            "domain",
            "email",
            "http_url",
            "uint16",
            "uint32",
            "uint64",
            "mtu",
            "mac",
            "mac_dot",
            "vlan",
            "docker_image",
        ]
        # Check if the kind is a valid predefined kind
        if data.get("name") in valid_js_kinds:
            kind["$ref"] = "#/$defs/{}".format(data["name"])
        # If not, check the kind type and build the schema based on some extra custom logic
        else:
            match data.get("name"):
                # For the choice kind, read the choices object
                case "choice":
                    if "choices" in data:
                        kind["enum"] = data["choices"]
                        kind.get("description", f"Choice of the below:\n{data['choices']}")
                    else:
                        self.log.error("Choice js_kind requires a choices object")
                        kind["description"] = "Choice js_kind requires a choices object"
                        kind["type"] = "null"
                # Default types
                case "string":
                    kind["type"] = "string"
                    kind["description"] = kind.get("description", "String")
                case "number":
                    kind["type"] = "number"
                    kind["description"] = kind.get("description", "Integer or Float")
                case "integer":
                    kind["type"] = "integer"
                    kind["description"] = kind.get("description", "Integer")
                case "boolean":
                    kind["type"] = "boolean"
                    kind["description"] = kind.get("description", "Boolean")
                case "null":
                    kind["type"] = "null"
                    kind["description"] = kind.get("description", "Null")
                case _:
                    # Check if the kind is user-defined from the user_defined_kinds class variable
                    if data.get("name") in self._view_user_defined_kinds():
                        kind["$ref"] = "#/$defs/{}".format(data["name"])
                    else:
                        self.log.error("Invalid js_kind (%s) detected, defaulting to Null", data)
                        kind["description"] = f"Invalid js_kind ({data}), defaulting to Null"
                        kind["type"] = "null"
        return kind
