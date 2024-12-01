![Build Status](https://github.com/commitconfirmed/jsnac/workflows/JSNAC%20TOX%20Suite/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/jsnac/badge/?version=latest)](https://jsnac.readthedocs.io/en/latest/?badge=latest) 


# JSNAC
JSON Schema (for) Network Automation Creator 

- [Overview](#overview)
- [Brief Example](#brief-example)
- [YAML Validation](#yaml-validation)
- [Detailed Example](#detailed-example)
- [Usage](#usage)

## Overview

The majority of Network and Infrastructure automation is done in YAML. Be it Ansible Host Variables, Network Device data to build a Jinja2 configuration with, or just a collection of data you want to run a script against to put into another product you have likely written a YAML file and have had to debug a typo or had to help another colleague build a new file for a new device.

In an ideal world you can (and should) put a lot of this data into a database or Network Source of Truth solution and pull from it so the validation is done for you. However, these solutions don't cover every use case so you will likely end up creating some YAML files here and there.

Using a JSON schema for validating & documenting your YAML is a good practice in a CI/CD world but is very cumbersome to create from scratch.

This project aims to simplify this whole process by helping you build a JSON schema using YAML syntax that has network and infrastructure templates (or sub-schemas) in mind.

Now you can hopefully catch those rare mistakes before you run that Playbook, create that configuration with a Jinja2 template or run a REST query to that Source of Truth or Telemetry solution :)

## Brief Example

Take a basic Ansible host_vars YAML file for a host below:

```yaml
chassis:
  hostname: "ceos-spine1"
  model: "ceos"
  device_type: "router"

system:
  domain_name: "example.com"
  ntp_servers: [ "10.0.0.1", "10.0.0.2" ]
    
interfaces:
  - if: "Loopback0"
    desc: "Underlay Loopback"
    ipv4: "10.0.0.101/32"
    ipv6: "2001:2:a1::1/128"
  - if: "Ethernet0"
    desc: "Management Interface"
    ipv4: "10.1.0.20/24"
```

You can simply write out how you would like to document & validate this data in YAML using kinds, and this program will write out a JSON schema you can use. 

```yaml
header:
  title: "Ansible host vars"

schema:
  chassis:
    title: "Chassis"
    type: "object"
    properties:
      hostname:
        kind: { name: "string" }
      model:
        kind: { name: "string" }
      device_type:
        kind: { name: "choice", choices: [ "router", "switch", "firewall", "load-balancer" ] }
  system:
    type: "object"
    properties:
      domain_name:
        kind: { name: "string" }
      ntp_servers:
        type: "array"
        items:
          kind: { name: "ipv4" } 
  interfaces:
    type: "array"
    items:
      type: "object"
      properties:
        if:
          kind: { name: "string" }
        desc:
          kind: { name: "string" }
        ipv4:
          kind: { name: "ipv4_cidr" }
        ipv6:
          kind: { name: "ipv6_cidr" }
```

```bash
(.venv) user@server:~/jsnac$ jsnac -f data/example-jsnac.yml 
[INFO] - jsnac - Starting JSNAC CLI
[INFO] - jsnac - Schema built in 0.0006 seconds
[INFO] - jsnac - Schema written to: jsnac.schema.json
[INFO] - jsnac - JSNAC CLI complete
```

## YAML Validation

To be able to validate the orginal YAML file or any new YAML file you create using this schema you first need to reference your JSON schema using the yaml-language-server comment at the top of your YAML file

```yaml
# yaml-language-server: $schema=jsnac.schema.json
---
chassis:
  hostname: "hostname"
```

Which language server you use is specific to your environment and editor that you use. For Visual Studio Code I recommend that you use the [Red Hat YAML Language Server](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) extension. Once installed you will now see that you will have automatic code completion, syntax highlighting, schema validation etc. while editing your YAML file.


## Detailed Example

We also have full support for writing your own titles, descriptions, kinds (sub-schemas), objects that are required, etc. A more fleshed out example of the same schema is below:

```yaml
header:
  id: "example-schema.json"
  title: "Ansible host vars"
  description: |
    Ansible host vars for my networking device. Requires the below objects:
    - chassis
    - system
    - interfaces

kinds:
  hostname:
    title: "Hostname"
    description: "Hostname of the device"
    type: "pattern"
    regex: "^[a-zA-Z0-9-]{1,63}$"

schema:
  chassis:
    title: "Chassis"
    description: | 
      Object containing Chassis information. Has the below properties: 
      hostname [required]: hostname
      model [required]: string
      device_type [required]: choice (router, switch, firewall, load-balancer)
    type: "object"
    properties:
      hostname:
        kind: { name: "hostname" }
      model:
        kind: { name: "string" }
      device_type:
        title: "Device Type"
        description: |
          Device Type options are:
          router, switch, firewall, load-balancer
        kind: { name: "choice", choices: [ "router", "switch", "firewall", "load-balancer" ] }
    required: [ "hostname", "model", "device_type" ]
  system:
    title: "System"
    description: |
      Object containing System information. Has the below properties:
      domain_name [required]: string
      ntp_servers [required]: list of ipv4 addresses
    type: "object"
    properties:
      domain_name:
        kind: { name: "string" }
      ntp_servers:
        title: "NTP Servers"
        description: "List of NTP servers"
        type: "array"
        items:
          kind: { name: "ipv4" } 
    required: [ "domain_name", "ntp_servers" ]
  interfaces:
    title: "Device Interfaces"
    description: |
      List of device interfaces. Each interface has the below properties:
      if [required]: string
      desc: string
      ipv4: ipv4_cidr
      ipv6: ipv6_cidr
    type: "array"
    items:
      type: "object"
      properties:
        if:
          kind: { name: "string" }
        desc:
          kind: { name: "string" }
        ipv4:
          kind: { name: "ipv4_cidr" }
        ipv6:
          kind: { name: "ipv6_cidr" }
      required: [ "if" ]
```

A full list of kinds are available in the [documentation](https://jsnac.readthedocs.io/en/latest/)

## Usage

### CLI

```bash
# Print the help message
jsnac -h

# Build a JSON schema from a YAML file (default file is jsnac.schema.json)
jsnac -f data/example-jsnac.yml

# Build a JSON schema from a YAML file and save it to a custom file
jsnac -f data/example-jsnac.yml -o my.schema.json

# Increase the verbosity of the output (this generates alot of messages as I use it for debugging)
jsnac -f data/example-jsnac.yml -v
```

### Library
```python
"""
This example demonstrates how to use the jsnac library to build a JSON schema from a YAML file in a Python script.
Example yml file is available here: <https://www.github.com/commitconfirmed/jsnac/blob/main/data/example-jsnac.yml>
"""
from jsnac.core.infer import SchemaInferer

def main():
    # Create a SchemaInferer object
    jsnac = SchemaInferer()

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
```