Introduction
============

The majority of Network and Infrastructure automation is done in YAML. Be it Ansible Host Variables, Network Device data to build a Jinja2 configuration with, or just a collection of data you want to run a script against to put into another product you have likely written a YAML file and have had to debug a typo or had to help another colleague build a new file for a new device.

In an ideal world you can (and should) put a lot of this data into a database or Network Source of Truth solution and pull from it so the validation is done for you. However, these solutions don't cover every use case so you will likely end up creating some YAML files here and there.

Using a JSON schema for validating & documenting your YAML is a good practice in a CI/CD world but is very cumbersome to create from scratch.

This project aims to simplify this whole process by helping you build a JSON schema using YAML syntax that has network and infrastructure templates (or sub-schemas) in mind.

Now you can hopefully catch those rare mistakes before you run that Playbook, create that configuration with a Jinja2 template or run a REST query to that Source of Truth or Telemetry solution :)

Overview
********

Take a basic Ansible host_vars YAML file for a host below:

.. code-block:: yaml

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

You can simply write out how you would like to validate this data, and this program will write out a JSON schema you can use. You can just also keep your existing data if you just want some basic type validation (string, integer, float, array, etc.).

.. code-block:: yaml

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

We also have full support for writing your own titles, descriptions, kinds (sub-schemas), objects that are required, etc. A more fleshed out example of the same schema is below:

.. code-block:: yaml

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

Motivation
**********

I wanted to find an easy and partially automated way to create a JSON schema from just a YAML file that I can use to practise CI/CD deployments using Ansible, Containerlab, etc. but the ones I found online were either too complex and didn't fit this use case or were created 10+ years ago and were no longer maintained. So I decided to create my own package that would fit my needs.

I have also never created a python project before, so I wanted to learn how to create a python package and publish it to PyPI.

Limitations
***********

- This is a very basic package in its current status and is not designed to be used in a production environment. 
- I am working on this in my free time and I am not a professional developer, so updates will be slow.
- Updates will likely completely change how this works as I continue to learn and grow my Python skills