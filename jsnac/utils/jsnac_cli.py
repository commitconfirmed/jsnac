import logging
import sys
import time
from argparse import ArgumentParser
from pathlib import Path

from jsnac import SchemaInferer, __version__


# Setup logging
def _setup_logging():  # noqa: ANN202
    log = logging.getLogger("jsnac")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def parse_args(args: str | None = None) -> ArgumentParser.parse_args:
    """Parse command-line arguments for the JSNAC CLI.

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
    """Main function for the JSNAC CLI.

    This function parses command-line arguments, sets up logging, and processes
    an input file (either JSON or YAML) to infer a schema using the SchemaInferer
    class. The inferred schema is then written to an output file.

    Args:
        args (str | None): Command-line arguments as a string. If None, arguments
                           will be parsed from sys.argv.

    """
    args = parse_args(args)
    log = _setup_logging()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    log.info("Starting JSNAC CLI")
    # File is required but checking anyway
    if args.file:
        input_file = Path(args.file)
        jsnac = SchemaInferer()
        if args.json:
            log.debug("Using JSON file: %s", args.file)
            with input_file.open() as f:
                jsnac.add_json(f.read())
                f.close()
        else:
            log.debug("Using YAML file: %s", args.file)
            with input_file.open() as f:
                jsnac.add_yaml(f.read())
                f.close()
        # Build the schema and record the time taken
        tic = time.perf_counter()
        schema = jsnac.build()
        toc = time.perf_counter()
        duration = toc - tic
        log.info("Schema built in %.4f seconds", duration)
        # Write the schema to a file
        schema_file = Path(args.output)
        with schema_file.open(mode="w") as f:
            f.write(schema)
        log.info("Schema written to: %s", schema_file)
    log.info("JSNAC CLI complete")
    sys.exit(0)


if __name__ == "__main__":
    # Import JSNAC in system path if run locally
    sys.path.insert(0, ".")
    main()
