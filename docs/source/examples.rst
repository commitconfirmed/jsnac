Examples
=============

Installation/Usage:
*******************

JSNAC can be installed using pip: ``pip install jsnac`` and can be used as either a command line tool or as a Python library in your own python project. The source code can also be found on `GitHub <https://www.github.com/commitconfirmed/jsnac>`_.

CLI usage:
**************************************************
.. code-block:: bash

    # Print the help message
    jsnac -h

    # Build a JSON schema from a YAML file (default file is jsnac.schema.json)
    jsnac -f data/example-jsnac.yml

    # Build a JSON schema from a YAML file and save it to a custom file
    jsnac -f data/example-jsnac.yml -o my.schema.json

    # Increase the verbosity of the output
    jsnac -f data/example-jsnac.yml -v

Library usage:
**************************************************
.. code-block:: python

    """
    This example demonstrates how to use the jsnac library to build a JSON schema 
    from a YAML file in a Python script. An example YAML file is available below:
    <https://www.github.com/commitconfirmed/jsnac/blob/main/data/example-jsnac.yml>
    """
    from jsnac.core.build import SchemaBuilder

    def main():
        # Create a SchemaInferer object
        jsnac = SchemaBuilder()

        # Load the YAML data however you like into the SchemaInferer object
        with open('data/example-jsnac.yml', 'r') as file:
            data = file.read()
        jsnac.add_yaml(data)

        # Loading from JSON directly is also supported if needed
        # jsnac.add_json(json_data)

        # Build the JSON schema
        schema = jsnac.build_schema()
        print(schema)

    if __name__ == '__main__':
        main()
