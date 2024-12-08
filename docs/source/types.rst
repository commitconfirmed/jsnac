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

**Example**

.. code-block:: yaml

    system:
      ip_address: 
        js_kind: { name: "ipv6_cidr" }

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

js_kind: email
******************

This type is used to validate a string against an email address.
The string will be validated against the below email address regex pattern.

.. code-block:: text

    ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$

**Example**

.. code-block:: yaml

    system:
      email_address: 
        js_kind: { name: "email" }

js_kind: http_url
******************

This type is used to validate a string against an HTTP URL.
The string will be validated against the below HTTP URL regex pattern.

.. code-block:: text

    ^(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})([/\\w .-]*)*\\??([^#\\s]*)?(#.*)?$

**Example**

.. code-block:: yaml

    system:
      sftp_server: 
        js_kind: { name: "http_url" }

js_kind: uint16
******************

This type is used to validate a string against a 16-bit unsigned integer (0 to 65535).

**Example**

.. code-block:: yaml

    bgp:
      as_number: 
        js_kind: { name: "uint16" }

js_kind: uint32
******************

This type is used to validate a string against a 32-bit unsigned integer (0 to 4294967295).

**Example**

.. code-block:: yaml

    bgp:
      as_number: 
        js_kind: { name: "uint32" }

js_kind: uint64
******************

This type is used to validate a string against a 64-bit unsigned integer (0 to 18446744073709551615).

**Example**

.. code-block:: yaml

    interface:
      statistics: 
        in_octets: { name: "uint64" }

js_kind: mtu
******************

This type is used to validate a string against a maximum transmission unit (MTU) value (68 to 9192).

**Example**

.. code-block:: yaml

    interface:
      mtu: 
        js_kind: { name: "mtu" }

js_kind: mac
******************

This type is used to validate a string against a MAC address (i.e ff:ff:ff:ff:ff:ff).
The string will be validated against the below MAC address regex pattern.

.. code-block:: text

    ^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$

**Example**

.. code-block:: yaml

    system:
      mac_address: 
        js_kind: { name: "mac" }

js_kind: mac_dot
******************

This type is used to validate a string against a MAC address with dot separator (i.e ffff.ffff.ffff).
The string will be validated against the below MAC address regex pattern.

.. code-block:: text

    ^([0-9A-Fa-f]{4}[.]){2}([0-9A-Fa-f]{4})$

**Example**

.. code-block:: yaml

    system:
      mac_address: 
        js_kind: { name: "mac_dot" }

js_kind: vlan
******************

This type is used to validate a string against a VLAN ID (1 to 4094).

**Example**

.. code-block:: yaml

    interface:
      vlan_id: 
        js_kind: { name: "vlan" }

js_kind: docker_image
*********************

This type is used to validate a string against a Docker image name.
The string will be validated against the below Docker image name regex pattern.

.. code-block:: text

    ^[a-z0-9]+(?:[._-][a-z0-9]+)*$

**Example**

.. code-block:: yaml

    system:
      docker_image: 
        js_kind: { name: "docker_image" }