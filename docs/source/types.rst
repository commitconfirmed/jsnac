JSNAC Kinds
===========

See the following sections for details on the included JSNAC kinds you can use in your YAML file(s).  

kind: pattern
*******************

This type is used to validate a string against a regular expression pattern.  
The pattern should be a valid regex pattern that will be used to validate the string. 
If you are going to use this more than once, it is recommended to use the kinds section so you can reuse the pattern.

**Example**

.. code-block:: yaml

    chassis:
      hostname: 
        kind: { name: "pattern", pattern: "^[a-zA-Z0-9-]{1,63}$" }

kind: choice
******************

This type is used to validate a string against a list of choices.
The choices should be a list of strings that the string will be validated against.

**Example**

.. code-block:: yaml

    chassis:
      type:
        kind: { name: "choice", choices: ["router", "switch", "firewall"] }

kind: domain
******************

This type is used to validate a string against a domain name.
The string will be validated against the below domain name regex pattern.

.. code-block:: text

    ^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$

**Example**

.. code-block:: yaml

    system:
      domain_name: 
        kind: { name: "domain" }

kind: ipv4
******************

This type is used to validate a string against an IPv4 address.
The string will be validated against the below IPv4 address regex pattern.

.. code-block:: text

    ^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$

**Example**

.. code-block:: yaml

    system:
      ip_address: 
        kind: { name: "ipv4" }