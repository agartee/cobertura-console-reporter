"""Application entrypoint"""
import argparse
import os
import sys

from cobertura_console_reporter import parser as coverage_parser
from cobertura_console_reporter import formatter


def main():
    """Application entry function"""
    arg_parser = argparse.ArgumentParser(description="Cobertura Console Reporter")
    arg_parser.add_argument(
        "--coverage-file",
        "-f",
        dest="coverage_file",
        required=True,
        help="Path to the coverage.cobertura.xml file produced by Coverlet.",
    )
    arg_parser.add_argument(
        "--package",
        "-p",
        dest="package_name",
        required=False,
        help="(Optional) Name of the .NET package (project) to display output for.",
    )
    args = arg_parser.parse_args()

    if not os.path.exists(args.coverage_file):
        print(f"File not found: {args.coverage_file}")
        sys.exit(1)

    coverage_items = coverage_parser.parse(args.coverage_file, args.package_name)
    formatted_result = formatter.format_coverage_items(coverage_items, colorize=True)

    print(formatted_result)


if __name__ == "__main__":
    main()
