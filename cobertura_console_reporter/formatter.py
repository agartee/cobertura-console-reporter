"""Contains formatting functions for CoverageItems intended for console output."""

import itertools
from typing import Iterator, List

from colorama import Fore, Style

from cobertura_console_reporter.coverage_item import CoverageItem
from cobertura_console_reporter.formatter_config import FormatterConfig


# pylint: disable=too-many-locals
def format_coverage_items(
    coverage_items: Iterator[CoverageItem], config: FormatterConfig
) -> str:
    """Formats a list of CoverageItems into a string suitable for console output.

    Args:
        coverage_items (Iterator[CoverageItem]): CoverageItems to display.
        config (FormatterConfig): Formatting configuration

    Returns:
        str: Formatted string intended for console output.
    """
    reset_color_val = Style.RESET_ALL if config.colorize is True else ""
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
            result += _build_namespace_data_row(key, items, row_format, config)

        for item in items:
            result += _build_data_row(key, item, row_format, config)

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
        if i in [class_name_col_idx, uncovered_line_numbers_col_idx]
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
    key: str, items: list[CoverageItem], row_format: str, config: FormatterConfig
) -> str:
    covered_line_percent = _format_percent(
        sum(item.covered_lines for item in items),
        sum(item.coverable_lines for item in items),
    )
    covered_branch_percent = _format_percent(
        sum(item.covered_branches for item in items),
        sum(item.branches for item in items),
    )

    ordered_group_column_values = [
        key,
        covered_line_percent,
        covered_branch_percent,
        "",  # uncovered lines column
    ]

    color = _get_row_color(config, covered_line_percent, covered_branch_percent)
    return f"{row_format.format(color=color, *ordered_group_column_values)}\n"


def _build_data_row(
    key: str, item: CoverageItem, row_format: str, config: FormatterConfig
) -> str:
    indent = "  " if key != "" else ""
    covered_line_percent = _format_percent(item.covered_lines, item.coverable_lines)
    covered_branch_percent = _format_percent(item.covered_branches, item.branches)

    ordered_column_values = [
        indent + item.class_name,
        covered_line_percent,
        covered_branch_percent,
        _compact_number_ranges(item.uncovered_line_numbers),
    ]

    color = _get_row_color(config, covered_line_percent, covered_branch_percent)
    return f"{row_format.format(color=color, *ordered_column_values)}\n"


def _format_percent(dividend: float, divisor: float) -> str:
    return format(dividend / divisor, ".0%") if divisor > 0 else "n/a"


def _get_row_color(
    config: FormatterConfig,
    covered_line_percent_str: str,
    covered_branch_percent_str: str,
) -> str:
    if config.colorize is True:
        if _below_percent(covered_line_percent_str, config.warning_threshold):
            return Fore.YELLOW
        if _below_percent(covered_branch_percent_str, config.warning_threshold):
            return Fore.YELLOW

        return Fore.GREEN

    return ""


def _below_percent(value_percent_str: str, threshold_percent: float) -> bool:
    if value_percent_str == "n/a" or not threshold_percent:
        return False

    value_percent = float(value_percent_str.rstrip("%"))

    return value_percent < threshold_percent


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
    for rng in ranges:
        if rng[0] == rng[1]:
            output.append(str(rng[0]))
        else:
            output.append(f"{rng[0]}-{rng[1]}")

    result = ", ".join(output)

    if len(result) > max_length:
        truncation_index = result[: max_length - 3].rfind(",")
        result = result[:truncation_index] + "..."

    return result
