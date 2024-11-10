JSNAC Types
===========

See the following sections for details on the jsnac_types you can use in your YAML file(s).  

jsnac_type: pattern
*******************

This type is used to validate a string against a regular expression pattern.  
The pattern should be a valid regex pattern that will be used to validate the string.  

**Example**

.. code-block:: yaml

    chassis:
      hostname:
        jsnac_type: pattern
        jsnac_pattern: "^ceos-[a-zA-Z]{1,16}[0-9]$"

jsnac_type: choice
******************

This type is used to validate a string against a list of choices.
The choices should be a list of strings that the string will be validated against.

**Example**

.. code-block:: yaml

    chassis:
      type:
        jsnac_type: choice
        jsnac_choices: ["router", "switch", "spine", "leaf"]

jsnac_type: domain
******************

This type is used to validate a string against a domain name.
The string will be validated against the below domain name regex pattern.

.. code-block:: text

    ^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$

**Example**

.. code-block:: yaml

    system:
      domain_name: 
        jsnac_type: domain