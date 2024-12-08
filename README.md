![Build Status](https://github.com/commitconfirmed/jsnac/workflows/JSNAC%20TOX%20Suite/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/jsnac/badge/?version=latest)](https://jsnac.readthedocs.io/en/latest/?badge=latest) 


# JSNAC
JSON Schema (for) Network Automation Creator 

- [Overview](#overview)
- [Installation](#installation)
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

## Installation

JSNAC can be installed using pip: ``pip install jsnac`` and can be used as either a command line tool or as a Python library in your own python project (See [Usage](#usage)).

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

You can simply write out how you would like to document & validate this data in a YAML file, and this program will generate a JSON schema you can use. 

```yaml
header:
  title: "Ansible host vars"

schema:
  chassis:
    title: "Chassis"
    properties:
      hostname:
        js_kind: { name: "string" }
      model:
        js_kind: { name: "string" }
      device_type:
        js_kind: { name: "choice", choices: [ "router", "switch", "firewall", "load-balancer" ] }
  system:
    properties:
      domain_name:
        js_kind: { name: "string" }
      ntp_servers:
        items:
          js_kind: { name: "ipv4" } 
  interfaces:
    items:
      properties:
        if:
          js_kind: { name: "string" }
        desc:
          js_kind: { name: "string" }
        ipv4:
          js_kind: { name: "ipv4_cidr" }
        ipv6:
          js_kind: { name: "ipv6_cidr" }
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

We also have full support for writing your own titles, descriptions, js_kinds (sub-schemas), objects that are required, etc. A more fleshed out example of the same schema is below:

```yaml
header:
  id: "example-schema.json"
  title: "Ansible host vars"
  description: |
    Ansible host vars for my networking device. Requires the below objects:
    - chassis
    - system
    - interfaces

js_kinds:
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
    properties:
      hostname:
        js_kind: { name: "hostname" }
      model:
        js_kind: { name: "string" }
      device_type:
        title: "Device Type"
        description: |
          Device Type options are:
          router, switch, firewall, load-balancer
        js_kind: { name: "choice", choices: [ "router", "switch", "firewall", "load-balancer" ] }
    required: [ "hostname", "model", "device_type" ]
  system:
    title: "System"
    description: |
      Object containing System information. Has the below properties:
      domain_name [required]: string
      ntp_servers [required]: list of ipv4 addresses
    properties:
      domain_name:
        js_kind: { name: "string" }
      ntp_servers:
        title: "NTP Servers"
        description: "List of NTP servers"
        items:
          js_kind: { name: "ipv4" } 
    required: [ "domain_name", "ntp_servers" ]
  interfaces:
    title: "Device Interfaces"
    description: |
      List of device interfaces. Each interface has the below properties:
      if [required]: string
      desc: string
      ipv4: ipv4_cidr
      ipv6: ipv6_cidr
    items:
      properties:
        if:
          js_kind: { name: "string" }
        desc:
          js_kind: { name: "string" }
        ipv4:
          js_kind: { name: "ipv4_cidr" }
        ipv6:
          js_kind: { name: "ipv6_cidr" }
      required: [ "if" ]
```

A full list of js_kinds are available in the [documentation](https://jsnac.readthedocs.io/en/latest/)

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
```