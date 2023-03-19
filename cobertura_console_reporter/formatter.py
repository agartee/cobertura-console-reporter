import itertools
from typing import Iterator

from colorama import Fore, Style

from cobertura_console_reporter.coverage_item import CoverageItem


def format_coverage_items(coverage_items: Iterator[CoverageItem], colorize:bool=False):
    class_name_width = max([len(ci.class_name) for ci in coverage_items] +
                           [len(ci.class_namespace) for ci in coverage_items])
    
    header_names = [
        "Class Name", 
        "Lines Coverable", 
        "Lines Covered", 
        "Branches", 
        "Branches Covered"
    ]

    header_lengths = [len(name) for name in header_names]
    header_lengths[0] = max([class_name_width, len(header_names[0])])

    reset_color = Style.RESET_ALL if colorize == True else ""

    header_formats = [f"{{:<{header_lengths[i]}}}" if i == 0 
                      else f"{{:>{header_lengths[i]}}}" 
                      for i in range(len(header_names))]
    header_format = "  |  ".join(header_formats)

    row_formats = [f"{{color}}{{:<{header_lengths[i]}}}{reset_color}" if i == 0 
                   else f"{{color}}{{:>{header_lengths[i]}}}{reset_color}" 
                   for i in range(len(header_names))]
    row_format = "  |  ".join(row_formats)

    separator_row_parts = [f"{'-' * (header_lengths[0] + 2)}"]
    separator_row_parts.extend(
        [f"{'-' * (length + 4)}" for length in header_lengths[1:]])
    separator_row = '|'.join(separator_row_parts)

    result = f"{separator_row}\n"
    result += f"{header_format.format(*header_names)}\n"
    result += f"{separator_row}\n"

    sorted_items = sorted(coverage_items, key=lambda x: x.class_namespace)
    grouped_items = itertools.groupby(sorted_items, key=lambda x: x.class_namespace)

    for key, group in grouped_items:
        items = list(group)

        if key != "":
            ordered_group_column_values = [
                key, 
                sum(item.coverable_lines for item in items), 
                sum(item.covered_lines for item in items), 
                sum(item.branches for item in items), 
                sum(item.covered_branches for item in items)
            ]

            color = Fore.GREEN if colorize == True else ""
            result += f"{row_format.format(color=color, *ordered_group_column_values)}\n"

        for item in items:
            indent = "  " if key != "" else ""

            ordered_column_values = [
                indent + item.class_name,
                item.coverable_lines, 
                item.covered_lines, 
                item.branches, 
                item.covered_branches
            ]
            
            color = Fore.GREEN if colorize == True else ""
            result += f"{row_format.format(color=color, *ordered_column_values)}\n"
    
    result += f"{separator_row}\n"

    return result
