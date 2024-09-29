import argparse
import time
import os
import logging

# Import JSNAC in system path if run locally
if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from jsnac import SchemaInferer, __version__

# Setup logging
def setup_logging():
    log = logging.getLogger("jsnac")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log

# Take in arguments from the CLI and run the application
def cli():
    parser = argparse.ArgumentParser(description="JSNAC CLI")
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show the version of the application'
    )
    parser.add_argument(
        '-c', '--config',
        type=str,
        required=True,
        help='Path to the configuration file'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='jsnac-schema.json',
        help='Path to the output file (default: jsnac-schema.json)'
    )
    return parser.parse_args()

def main():
    args = cli()
    log = setup_logging()
    log.info("Starting JSNAC CLI")
    if args.version:
        log.info(f"JSNAC version {__version__}")
    if args.config:
        log.info(f"Using YAML file: {args.config}")
    jsnac = SchemaInferer()
    jsnac.add_yaml(open(args.config).read())
    schema = jsnac.build()
    # Write the schema to a file
    schema_file = args.output
    with open(schema_file, 'w') as f:
        f.write(schema)
    log.info(f"Schema written to: {schema_file}")
    log.info("JSNAC CLI complete")
        

if __name__ == "__main__":
    main()