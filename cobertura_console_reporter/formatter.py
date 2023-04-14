"""Contains formatting functions for CoverageItems intended for console output."""

import itertools
from typing import Iterator, List

from colorama import Fore, Style

from cobertura_console_reporter.coverage_item import CoverageItem


# pylint: disable=too-many-locals
def format_coverage_items(
    coverage_items: Iterator[CoverageItem], colorize: bool = False
) -> str:
    """Formats a list of CoverageItems into a string suitable for console output.

    Args:
        coverage_items (Iterator[CoverageItem]): CoverageItems to display.
        colorize (bool, optional): Colorize by test-coverage status. Defaults to False.

    Returns:
        str: Formatted string intended for console output.
    """
    class_name_width = max(
        [len(ci.class_name) for ci in coverage_items]
        + [len(ci.class_namespace) for ci in coverage_items]
    )

    header_names = [
        "Class Name",
        "Lines Coverable",
        "Lines Covered",
        "Branches",
        "Branches Covered",
        "Uncovered Lines",
    ]

    header_lengths = [len(name) for name in header_names]
    header_lengths[0] = max([class_name_width, len(header_names[0])])

    reset_color = Style.RESET_ALL if colorize is True else ""

    header_formats = [
        f"{{:<{header_lengths[i]}}}" if i == 0 else f"{{:>{header_lengths[i]}}}"
        for i in range(len(header_names))
    ]
    header_format = "  |  ".join(header_formats)

    class_name_col_idx = 0
    uncovered_line_numbers_col_idx = 5

    row_formats = [
        f"{{color}}{{:<{header_lengths[i]}}}{reset_color}"
        if i == class_name_col_idx or i == uncovered_line_numbers_col_idx
        else f"{{color}}{{:>{header_lengths[i]}}}{reset_color}"
        for i in range(len(header_names))
    ]
    row_format = "  |  ".join(row_formats)

    separator_row_parts = [f"{'-' * (header_lengths[0] + 2)}"]
    separator_row_parts.extend(
        [f"{'-' * (length + 4)}" for length in header_lengths[1:]]
    )
    separator_row = "|".join(separator_row_parts)

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
                sum(item.covered_branches for item in items),
                "",
            ]

            color = Fore.GREEN if colorize is True else ""
            result += (
                f"{row_format.format(color=color, *ordered_group_column_values)}\n"
            )

        for item in items:
            indent = "  " if key != "" else ""

            ordered_column_values = [
                indent + item.class_name,
                item.coverable_lines,
                item.covered_lines,
                item.branches,
                item.covered_branches,
                compact_number_ranges(item.uncovered_line_numbers),
            ]

            color = Fore.GREEN if colorize is True else ""
            result += f"{row_format.format(color=color, *ordered_column_values)}\n"

    result += f"{separator_row}\n"

    return result


def compact_number_ranges(numbers: List[int], max_length=15) -> str:
    """Rewrites sequenced numbers into a range and truncates output if it exceeds the
    max length.

    Args:
        numbers (List[int]): A list of numbers
        max_length (int, optional): number of characters to allow for the output. Defaults to 15.

    Returns:
        str: Formatted string.
    """
    if not numbers:
        return ""

    ranges = []
    start = numbers[0]
    end = numbers[0]

    for i in range(1, len(numbers)):
        if numbers[i] == end + 1:
            end = numbers[i]
        else:
            ranges.append((start, end))
            start = end = numbers[i]
    ranges.append((start, end))

    output = []
    for r in ranges:
        if r[0] == r[1]:
            output.append(str(r[0]))
        else:
            output.append(f"{r[0]}-{r[1]}")

    result = ", ".join(output)

    if len(result) > max_length:
        truncation_index = result[: max_length - 3].rfind(",")
        result = result[:truncation_index] + "..."

    return result
