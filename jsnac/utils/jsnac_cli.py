#!/usr/bin/env python3
"""
JSNAC CLI Utility

This module provides a command-line interface (CLI) for the JSNAC application, which is used to convert YAML files
to JSON and build schemas. It includes functions for setting up logging, parsing command-line arguments,
and processing input files to infer schemas.

Functions:
    _setup_logging() -> logging.Logger:
        Sets up logging for the JSNAC CLI.

    parse_args(args: str | None = None) -> Namespace:
        Parses command-line arguments for the JSNAC CLI.

    main(args: str | None = None) -> None:
        Main function for the JSNAC CLI. Parses command-line arguments, sets up logging,
        and processes input files to infer schemas.
"""

# Dependencies (Standard Library)
import logging
import sys
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from jsnac import SchemaInferer, __version__


def _setup_logging() -> logging.Logger:
    """
    Set up logging for the JSNAC CLI.

    Returns:
        logging.Logger: A logger instance for the JSNAC CLI.

    """
    log = logging.getLogger("jsnac")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def parse_args(args: str | None = None) -> Namespace:
    """
    Parse command-line arguments for the JSNAC CLI.

    Args:
        args (str | None): A string of arguments to parse. If None, the arguments
                           will be taken from sys.argv.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.

    Arguments:
        --version: Show the version of the application.
        -f, --file (str, required): Path to the YAML file to convert to JSON and build a schema.
        -j, --json: Skip converting YAML to JSON and use JSON directly.
        -o, --output (str, default="jsnac.schema.json"): Path to the output file.
        -i, --infer: Attempt to infer the schema on an unmodified YAML/JSON file [In Development].
        -v, --verbose: Increase log verbosity.

    """
    parser = ArgumentParser(description="JSNAC CLI")
    parser.add_argument(
        "--version",
        action="version",
        version=f"JSNAC version {__version__}",
        help="Show the version of the application",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Path to the YAML file to convert to JSON and build a schema",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Skip converting YAML to JSON and use JSON directly",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="jsnac.schema.json",
        help="Path to the output file (default: jsnac.schema.json)",
    )
    parser.add_argument(
        "-i",
        "--infer",
        action="store_true",
        help="Attempt to infer the schema on an unmodified YAML/JSON file [In Development]",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity")
    return parser.parse_args(args)


def main(args: str | None = None) -> None:
    """
    Main function for the JSNAC CLI.

    This function parses command-line arguments, sets up logging, and processes
    an input file (either JSON or YAML) to infer a schema using the SchemaInferer
    class. The inferred schema is then written to an output file.

    Args:
        args (str | None): Command-line arguments as a string. If None, arguments
                           will be parsed from sys.argv.

    """
    flags: Namespace = parse_args(args)
    log = _setup_logging()
    if flags.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    log.info("Starting JSNAC CLI")
    # File is required but checking anyway
    if flags.file:
        input_file = Path(flags.file)
        jsnac = SchemaInferer()
        if flags.json:
            log.debug("Using JSON file: %s", flags.file)
            with input_file.open() as f:
                jsnac.add_json(f.read())
                f.close()
        else:
            log.debug("Using YAML file: %s", flags.file)
            with input_file.open() as f:
                jsnac.add_yaml(f.read())
                f.close()
        # Build the schema and record the time taken
        tic = time.perf_counter()
        schema = jsnac.build_schema()
        toc = time.perf_counter()
        duration = toc - tic
        log.info("Schema built in %.4f seconds", duration)
        # Write the schema to a file
        schema_file = Path(flags.output)
        with schema_file.open(mode="w") as f:
            f.write(schema)
        log.info("Schema written to: %s", schema_file)
    log.info("JSNAC CLI complete")
    sys.exit(0)


if __name__ == "__main__":
    # Import JSNAC in system path if run locally
    sys.path.insert(0, ".")
    main()
