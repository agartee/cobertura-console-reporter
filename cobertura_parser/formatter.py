from typing import Iterator

from cobertura_parser.coverage_item import CoverageItem


def format_coverage_items(coverage_items: Iterator[CoverageItem]):
    class_name_width = max(len(ci.name) for ci in coverage_items)
    
    header_names = [
        "Class Name", 
        "Lines Coverable", 
        "Lines Covered", 
        "Branches", 
        "Branches Covered"
    ]

    header_lengths = [len(name) for name in header_names]
    header_lengths[0] = class_name_width

    header_formats = [f"{{:<{header_lengths[i]}}}" 
                      if i == 0 else f"{{:>{header_lengths[i]}}}" 
                      for i in range(len(header_names))]
    row_format = "  |  ".join(header_formats)

    separator_row_parts = [f"{'-' * (header_lengths[0] + 2)}"]
    separator_row_parts.extend(
        [f"{'-' * (length + 4)}" for length in header_lengths[1:]])
    separator_row = '|'.join(separator_row_parts)

    result = f"{separator_row}\n"
    result += f"{row_format.format(*header_names)}\n"
    result += f"{separator_row}\n"

    for ci in coverage_items:
        ordered_column_values = [
            ci.name, 
            ci.coverable_lines, 
            ci.covered_lines, 
            ci.branches, 
            ci.covered_branches
        ]
        
        result += f"{row_format.format(*ordered_column_values)}\n"
    
    result += f"{separator_row}\n"

    return result
