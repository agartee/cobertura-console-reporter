import os
import sys

from cobertura_console_reporter import parser
from cobertura_console_reporter import formatter


if __name__ == "__main__":
    print(sys.argv)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python -m cobertura_console_reporter <path_to_coverage_cobertura_xml_file> [package_name]")
        sys.exit(1)

    coverage_file_path = sys.argv[1]
    if not os.path.exists(coverage_file_path):
        print(f"File not found: {coverage_file_path}")
        sys.exit(1)

    package_name = sys.argv[2] if len(sys.argv) > 2 else None
    coverage_items = parser.parse(coverage_file_path, package_name)
    formatted_result = formatter.format_coverage_items(coverage_items, colorize=True)

    print(formatted_result)
