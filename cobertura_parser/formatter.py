from typing import Iterator

from cobertura_parser.coverage_item import CoverageItem


def format_coverage_items(coverage_items: Iterator[CoverageItem]):
    class_name_width = max(len(ci.name) for ci in coverage_items)
    
    header_names = ["Class Name", "Lines Coverable", "Lines Covered", "Branches", "Branches Covered"]
    header_lengths = [len(name) for name in header_names]
    header_format = f"{{:<{class_name_width}}}  |  {{:>{header_lengths[1]}}}  |  {{:>{header_lengths[2]}}}  |  {{:>{header_lengths[3]}}}  |  {{:>{header_lengths[4]}}}"
    row_format = f"{{:<{class_name_width}}}  |  {{:>{header_lengths[1]}}}  |  {{:>{header_lengths[2]}}}  |  {{:>{header_lengths[3]}}}  |  {{:>{header_lengths[4]}}}"
    
    separator_char = '-'
    separator = f"{separator_char * (class_name_width+2)}|{separator_char * (header_lengths[1]+4)}|{separator_char * (header_lengths[2]+4)}|{separator_char * (header_lengths[3]+4)}|{separator_char * (header_lengths[4]+4)}"
    
    result = f"{separator}\n"
    result += f"{header_format.format(*header_names)}\n"
    result += f"{separator}\n"

    for ci in coverage_items:
        result += f"{row_format.format(ci.name, ci.coverable_lines, ci.covered_lines, ci.branches, ci.covered_branches)}\n"
    
    result += f"{separator}\n"

    return result
