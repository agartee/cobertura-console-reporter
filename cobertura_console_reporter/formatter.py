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
    reset_color_val = Style.RESET_ALL if colorize is True else ""
    class_name_length = _calc_class_name_length(coverage_items)

    header_names = [
        "Class Name",
        "% Lines",
        "% Branches",
        "Uncovered Line #s",
    ]
    header_lengths = [len(name) for name in header_names]
    header_lengths[0] = max([class_name_length, len(header_names[0])])
    header_format = "  |  ".join(
        _build_header_row_formats(header_names, header_lengths)
    )

    class_name_col_idx = 0
    uncovered_line_numbers_col_idx = 3
    row_formats = _build_data_row_format(
        reset_color_val,
        header_names,
        header_lengths,
        class_name_col_idx,
        uncovered_line_numbers_col_idx,
    )
    row_format = "  |  ".join(row_formats)

    separator_row = _build_separator_row(header_lengths)

    result = f"{separator_row}\n"
    result += f"{header_format.format(*header_names)}\n"
    result += f"{separator_row}\n"

    grouped_items = itertools.groupby(
        sorted(coverage_items, key=lambda x: x.class_namespace),
        key=lambda x: x.class_namespace,
    )

    for key, group in grouped_items:
        items = list(group)

        if key != "":
            result += _build_namespace_data_row(key, items, row_format, colorize)

        for item in items:
            result += _build_data_row(key, item, row_format, colorize)

    result += f"{separator_row}\n"

    return result


def _build_separator_row(header_lengths: list[int]) -> str:
    separator_row_parts = [f"{'-' * (header_lengths[0] + 2)}"]
    separator_row_parts.extend(
        [f"{'-' * (length + 4)}" for length in header_lengths[1:]]
    )
    return "|".join(separator_row_parts)


def _build_data_row_format(
    reset_color_val,
    header_names,
    header_lengths,
    class_name_col_idx,
    uncovered_line_numbers_col_idx,
):
    return [
        f"{{color}}{{:<{header_lengths[i]}}}{reset_color_val}"
        if i == class_name_col_idx or i == uncovered_line_numbers_col_idx
        else f"{{color}}{{:>{header_lengths[i]}}}{reset_color_val}"
        for i in range(len(header_names))
    ]


def _build_header_row_formats(header_names, header_lengths):
    return [
        f"{{:<{header_lengths[i]}}}" if i == 0 else f"{{:>{header_lengths[i]}}}"
        for i in range(len(header_names))
    ]


def _calc_class_name_length(coverage_items):
    return max(
        [len(ci.class_name) for ci in coverage_items]
        + [len(ci.class_namespace) for ci in coverage_items]
    )


def _build_namespace_data_row(
    key: str, items: list[CoverageItem], row_format: str, colorize: bool
) -> str:
    ordered_group_column_values = [
        key,
        _format_percent(
            sum(item.covered_lines for item in items),
            sum(item.coverable_lines for item in items),
        ),
        _format_percent(
            sum(item.covered_branches for item in items),
            sum(item.branches for item in items),
        ),
        "",
    ]

    color = Fore.GREEN if colorize is True else ""
    return f"{row_format.format(color=color, *ordered_group_column_values)}\n"


def _build_data_row(
    key: str, item: CoverageItem, row_format: str, colorize: bool
) -> str:
    indent = "  " if key != "" else ""

    ordered_column_values = [
        indent + item.class_name,
        _format_percent(item.covered_lines, item.coverable_lines),
        _format_percent(item.covered_branches, item.branches),
        _compact_number_ranges(item.uncovered_line_numbers),
    ]

    color = Fore.GREEN if colorize is True else ""
    return f"{row_format.format(color=color, *ordered_column_values)}\n"


def _format_percent(dividend: float, divisor: float) -> str:
    return format(dividend / divisor, ".0%") if divisor > 0 else "n/a"


def _compact_number_ranges(numbers: List[int], max_length=17) -> str:
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
