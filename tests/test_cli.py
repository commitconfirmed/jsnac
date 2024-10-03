from jsnac.utils.jsnac_cli import cli
from jsnac.utils.jsnac_cli import main
import pytest

# Test CLI with no arguments
def test_cli(capsys) -> None:
    # Test CLI with no arguments
    with pytest.raises(SystemExit):
        cli()
    output = capsys.readouterr()
    assert "error: the following arguments are required" in output.err

# Test CLI with help argument
def test_cli_help(capsys) -> None:
    with pytest.raises(SystemExit):
        cli(["-h"])
    output = capsys.readouterr()
    assert "JSNAC CLI\n\noptions:" in output.out

# Test CLI with version argument
def test_cli_version(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    output = capsys.readouterr()
    assert "JSNAC version" in output.out

# Test CLI with config argument
def test_cli_config(capsys) -> None:
    with pytest.raises(SystemExit):
        main(["-c", "test.yml"])
    output = capsys.readouterr()
    assert "Schema written to: jsnac.schema.json" in output.out