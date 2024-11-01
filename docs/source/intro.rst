Introduction
============

``jsnac`` is a Python package that builds JSON schemas from specifally modified YAML files. It can also be used to build a basic schema with unmodified YAML files. It is designed to be used in network automation and network as code (NaC) projects. The package is built on top of the PyYAML and JSON Schema libraries.

The package is designed to be used as a command line tool, but can also be used as a Python library. The command line tool is called `jsnac` and is installed when the package is installed. The command line tool can be used to build JSON schemas from YAML files. The Python library can be used to build JSON schemas from YAML files in a Python script.

Python 3.10 or later is required to use this package.

Motivation
**********

I wanted to find an easy and partially automated way to create a JSON schema from just a YAML file that I can use to practise CI/CD deployments using Ansible, Containerlab, etc. but the ones I found online were either too complex and didn't fit this use case or were created 10+ years ago and were no longer maintained. So I decided to create my own package that would fit my needs.

I have also never created a python project before, so I wanted to learn how to create a python package and publish it to PyPI.

Limitations
***********

- This is a very basic package in its current status and is not designed to be used in a production environment. 
- I am working on this in my free time and I am not a professional developer, so updates will be slow.