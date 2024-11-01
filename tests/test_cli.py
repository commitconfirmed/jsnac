#!/usr/bin/env python3
import pytest

from jsnac.utils.jsnac_cli import main


# Test CLI with no arguments
def test_cli(capsys) -> None:
    with pytest.raises(SystemExit):
        main()
    output = capsys.readouterr()
    assert "error: the following arguments are required" in output.err


# Test CLI with help argument
def test_cli_help(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["-h"])
    output = capsys.readouterr()
    assert "JSNAC CLI\n\noptions:" in output.out


# Test CLI with version argument
def test_cli_version(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    output = capsys.readouterr()
    assert "JSNAC version" in output.out


# Test CLI with file argument and included YAML file using JSNAC definitions
def test_cli_file_yaml_jsnac(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["-f", "data/example-jsnac.yml"])
    output = capsys.readouterr()
    assert "JSNAC CLI complete" in output.err


# Test CLI with file argument and regular YAML file
def test_cli_file_yaml(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["-f", "data/example.yml"])
    output = capsys.readouterr()
    assert "JSNAC CLI complete" in output.err


# Test CLI with file argument and included JSON file using JSNAC definitions
def test_cli_file_json(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["-f", "data/example-jsnac.json", "-j"])
    output = capsys.readouterr()
    assert "JSNAC CLI complete" in output.err
