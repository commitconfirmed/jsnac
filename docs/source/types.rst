JSNAC Kinds
===========

See the following sections for details on the included JSNAC kinds you can use in your YAML file(s).  

js_kind: choice
******************

This type is used to validate a string against a list of choices.
The choices should be a list of strings that the string will be validated against.

**Example**

.. code-block:: yaml

    chassis:
      type:
        js_kind: { name: "choice", choices: ["router", "switch", "firewall"] }

js_kind: ipv4
******************

This type is used to validate a string against an IPv4 address.
The string will be validated against the below IPv4 address regex pattern.

.. code-block:: text

    ^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])$

**Example**

.. code-block:: yaml

    system:
      ip_address: 
        js_kind: { name: "ipv4" }

js_kind: ipv6
******************

This type is used to validate a string against an IPv6 address.
The string will be validated against the below IPv6 address regex pattern.

.. code-block:: text

    ^(([a-fA-F0-9]{1,4}|):){1,7}([a-fA-F0-9]{1,4}|:)$

**Example**

.. code-block:: yaml

    system:
      ip_address: 
        js_kind: { name: "ipv6" }

js_kind: ipv4_cidr
******************

This type is used to validate a string against an IPv4 CIDR address.
The string will be validated against the below IPv4 CIDR address regex pattern.

.. code-block:: text

    ^((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])/(1[0-9]|[0-9]|2[0-9]|3[0-2])$

**Example**

.. code-block:: yaml

    system:
      ip_address: 
        js_kind: { name: "ipv4_cidr" }

js_kind: ipv6_cidr
******************

This type is used to validate a string against an IPv6 CIDR address.
The string will be validated against the below IPv6 CIDR address regex pattern.

.. code-block:: text

    ^(([a-fA-F0-9]{1,4}|):){1,7}([a-fA-F0-9]{1,4}|:)/(32|36|40|44|48|52|56|60|64|128)$


js_kind: mac
******************

This type is used to validate a string against a MAC address.
The string will be validated against the below MAC address regex pattern.

.. code-block:: text

    ^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$

**Example**

.. code-block:: yaml

    system:
      mac_address: 
        js_kind: { name: "mac" }

js_kind: domain
******************

This type is used to validate a string against a domain name.
The string will be validated against the below domain name regex pattern.

.. code-block:: text

    ^([a-zA-Z0-9-]{1,63}\\.)+[a-zA-Z]{2,63}$

**Example**

.. code-block:: yaml

    system:
      domain_name: 
        js_kind: { name: "domain" }