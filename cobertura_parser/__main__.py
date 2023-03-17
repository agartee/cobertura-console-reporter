import os
import sys

from cobertura_parser import parser
from cobertura_parser import formatter


if __name__ == "__main__":
    print("working on it...")

    if len(sys.argv) != 2:
        print("Usage: python -m cobertura_parser <path_to_coverage_cobertura_xml_file>")
        sys.exit(1)

    coverage_file_path = sys.argv[1]

    if not os.path.exists(coverage_file_path):
        print(f"File not found: {coverage_file_path}")
        sys.exit(1)


    coverage_items = parser.parse(coverage_file_path)
    print(formatter.format_coverage_items(coverage_items, colorize=True))
