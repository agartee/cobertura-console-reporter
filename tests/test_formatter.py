import textwrap

from colorama import Fore, Style

from cobertura_console_reporter.coverage_item import CoverageItem
from cobertura_console_reporter.formatter import format_coverage_items
from cobertura_console_reporter.formatter_config import FormatterConfig


def test_format_coverage_items_returns_formatted_string():
    items = [
        CoverageItem(
            name="SampleApp.Domain.Services.FirstService",
            file_name="Services\\FirstService.cs",
            coverable_lines=100,
            covered_lines=65,
            uncovered_line_numbers=[10, 11],
            branches=12,
            covered_branches=6,
        ),
        CoverageItem(
            name="SampleApp.Domain.Services.SecondService",
            file_name="Services\\SecondService.cs",
            coverable_lines=100,
            covered_lines=65,
            uncovered_line_numbers=[10, 11],
            branches=12,
            covered_branches=6,
        ),
    ]

    expected = f"""\
        ---------------------------|-----------|--------------|---------------------
        Class Name                 |  % Lines  |  % Branches  |  Uncovered Line #s
        ---------------------------|-----------|--------------|---------------------
        SampleApp.Domain.Services  |      65%  |         50%  |                   
          FirstService             |      65%  |         50%  |  10-11            
          SecondService            |      65%  |         50%  |  10-11            
        ---------------------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_namespace_and_class_names_shorter_than_header_returns_formatted_string():
    items = [
        CoverageItem(
            name="A.B.C",
            file_name="C.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[10, 11],
            branches=25,
            covered_branches=10,
        )
    ]

    expected = f"""\
        ------------|-----------|--------------|---------------------
        Class Name  |  % Lines  |  % Branches  |  Uncovered Line #s
        ------------|-----------|--------------|---------------------
        A.B         |      50%  |         40%  |                   
          C         |      50%  |         40%  |  10-11            
        ------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_class_does_not_have_namespace_returns_formatted_string():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[10, 11],
            branches=25,
            covered_branches=10,
        )
    ]

    expected = f"""\
        ------------|-----------|--------------|---------------------
        Class Name  |  % Lines  |  % Branches  |  Uncovered Line #s
        ------------|-----------|--------------|---------------------
        Program     |      50%  |         40%  |  10-11            
        ------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_uncovered_lines_value_exceeds_max_length_returns_formatted_string():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[10, 11, 13, 15, 17, 19, 21],
            branches=25,
            covered_branches=10,
        )
    ]

    expected = f"""\
        ------------|-----------|--------------|---------------------
        Class Name  |  % Lines  |  % Branches  |  Uncovered Line #s
        ------------|-----------|--------------|---------------------
        Program     |      50%  |         40%  |  10-11, 13, 15... 
        ------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_no_uncovered_lines_exist_for_file_returns_formatted_string():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[],
            branches=25,
            covered_branches=10,
        )
    ]

    expected = f"""\
        ------------|-----------|--------------|---------------------
        Class Name  |  % Lines  |  % Branches  |  Uncovered Line #s
        ------------|-----------|--------------|---------------------
        Program     |      50%  |         40%  |                   
        ------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_no_branches_returns_formatted_string():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[],
            branches=0,
            covered_branches=0,
        )
    ]

    expected = f"""\
        ------------|-----------|--------------|---------------------
        Class Name  |  % Lines  |  % Branches  |  Uncovered Line #s
        ------------|-----------|--------------|---------------------
        Program     |      50%  |         n/a  |                   
        ------------|-----------|--------------|---------------------
        """

    result = format_coverage_items(items, FormatterConfig.no_color())

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_colorized_and_branch_coverage_above_threshold_returns_green_text():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=10,
            covered_lines=10,
            uncovered_line_numbers=[],
            branches=0,
            covered_branches=0,
        )
    ]

    result = format_coverage_items(
        items, FormatterConfig(colorize=True, warning_threshold=90)
    )

    assert Fore.GREEN in result


def test_format_coverage_items_when_colorized_and_line_coverage_below_threshold_returns_yellow_text():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=10,
            covered_lines=5,
            uncovered_line_numbers=[5, 6, 7, 8, 9],
            branches=5,
            covered_branches=0,
        )
    ]

    result = format_coverage_items(
        items, FormatterConfig(colorize=True, warning_threshold=90)
    )

    assert Fore.YELLOW in result


def test_format_coverage_items_when_colorized_and_branch_coverage_below_threshold_returns_yellow_text():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=10,
            covered_lines=10,
            uncovered_line_numbers=[],
            branches=5,
            covered_branches=2,
        )
    ]

    result = format_coverage_items(
        items, FormatterConfig(colorize=True, warning_threshold=90)
    )

    assert Fore.YELLOW in result
