# JSNAC
JSON Schema (for) Network as Code 

## Overview

The majority of Network and Infrastructure automation is done in YAML. Be it Ansible Host Variables, Network Device data to build a Jinja2 configuration with, or just a collection of data you want to run a script against to put into another product you have likely written a YAML file and have had to debug a typo or had to help another colleague build a new file for a new device.

In an ideal world you can (and should) put a lot of this data into a database or Network Source of Truth solution and pull from it so the validation is done for you. However, these solutions don't cover every case and generally don't play nice with a GIT CI/CD process so you still will likely end up creating some YAML files here and there.

Using a JSON schema for validating your YAML is a good practice in a CI/CD world but is very cumbersome to create from scratch.

This project aims to simplify this whole process to help you build a decent JSON schema base from a YAML file with network and infrastructure data definitions in mind. 

Now you can hopefully catch those rare mistakes before you run that Playbook, create that configuration with a Jinja2 template or run a REST query to that Source of Truth or Telemetry solution :)

## Brief Example

Take a basic Ansible host_vars YAML file for a host below:

```yaml
chassis:
    hostname: "ceos-spine1"
    model: "ceos"
    type: "router"

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

You can simply write out how you would like to validate this data, and this program will write out a JSON schema you can use. You can just also keep your existing data if you just want some basic type validation (string, integer, float, array, etc.).

```yaml
chassis:
  hostname:
    jsnac_type: pattern
    jsnac_pattern: "^ceos-[a-zA-Z]{1,16}[0-9]$"
  model: "ceos"
  type:
    jsnac_type: choice
    jsnac_choices: ["router", "switch", "spine", "leaf"]

system:
  domain_name: 
    jsnac_type: domain
  ntp_servers:
    jsnac_type: ipv4
  
interfaces:
  - if:
      jsnac_type: string
    desc: 
      jsnac_type: string
    ipv4: 
      jsnac_type: ipv4_cidr
    ipv6:
      jsnac_type: ipv6_cidr
```

Alternatively, you can also just use dictionaries inplace:

```yaml
chassis:
  hostname: { jsnac_type: pattern, jsnac_pattern: "^ceos-[a-zA-Z]{1,16}[0-9]$" }
  model: "ceos"
  type: { jsnac_type: choice, jsnac_choices: ["router", "switch", "spine", "leaf"] }

system:
  domain_name: { jsnac_type: domain }
  ntp_servers: { jsnac_type: ipv4 }
  
interfaces:
  - if: { jsnac_type: string }
    desc: { jsnac_type: string }
    ipv4: { jsnac_type: ipv4_cidr }
    ipv6: { jsnac_type: ipv6_cidr }
```

A full list of jsnac_types is available in the documentation

## Usage

You can use jsnac from the command line or by importing it and calling InferSchema?
