import sys
import time
import logging
from argparse import ArgumentParser
from jsnac import SchemaInferer, __version__

# Setup logging
def setup_logging():
    log = logging.getLogger("jsnac")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] - %(name)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log

# Take in arguments from the CLI and run JSNAC
def parse_args(args=None) -> ArgumentParser.parse_args:
    parser = ArgumentParser(description="JSNAC CLI")
    parser.add_argument(
        '--version',
        action='version',
        version=f'JSNAC version {__version__}',
        help='Show the version of the application'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help='Path to the YAML file to convert to JSON and build a schema'
    )
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Skip converting YAML to JSON and use JSON directly'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='jsnac.schema.json',
        help='Path to the output file (default: jsnac.schema.json)'
    )
    parser.add_argument(
        '-i', '--infer',
        action='store_true',
        help='Attempt to infer the schema on an unmodified YAML/JSON file [In Development]'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increase log verbosity'
    )
    return parser.parse_args(args)

def main(args=None) -> None:
    args = parse_args(args)
    log = setup_logging()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    log.info("Starting JSNAC CLI")
    # File is required but checking anyway
    if args.file:
        jsnac = SchemaInferer()
        if args.json:
            log.debug(f"Using JSON file: {args.file}")
            jsnac.add_json(open(args.file).read())
        else:
            log.debug(f"Using YAML file: {args.file}")
            jsnac.add_yaml(open(args.file).read())
        # Build the schema and record the time taken
        tic = time.perf_counter()
        schema = jsnac.build()
        toc = time.perf_counter()
        log.info(f"Schema built in {toc - tic:0.4f} seconds")
        # Write the schema to a file
        schema_file = args.output
        with open(schema_file, 'w') as f:
            f.write(schema)
        log.info(f"Schema written to: {schema_file}")
    log.info("JSNAC CLI complete")
    sys.exit(0)      

if __name__ == "__main__":
    # Import JSNAC in system path if run locally
    sys.path.insert(0, ".")
    main()