import textwrap

from cobertura_console_reporter.coverage_item import CoverageItem
from cobertura_console_reporter.formatter import format_coverage_items


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

    expected = """\
        ---------------------------|-------------------|-----------------|------------|--------------------|-------------------
        Class Name                 |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered  |  Uncovered Lines
        ---------------------------|-------------------|-----------------|------------|--------------------|-------------------
        SampleApp.Domain.Services  |              200  |            130  |        24  |                12  |                 
          FirstService             |              100  |             65  |        12  |                 6  |  10-11          
          SecondService            |              100  |             65  |        12  |                 6  |  10-11          
        ---------------------------|-------------------|-----------------|------------|--------------------|-------------------
        """

    result = format_coverage_items(items, colorize=False)

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

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered  |  Uncovered Lines
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        A.B         |              100  |             50  |        25  |                10  |                 
          C         |              100  |             50  |        25  |                10  |  10-11          
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        """

    result = format_coverage_items(items, colorize=False)

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

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered  |  Uncovered Lines
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Program     |              100  |             50  |        25  |                10  |  10-11          
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        """

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_uncovered_lines_value_exceeds_max_length_returns_formatted_string():
    items = [
        CoverageItem(
            name="Program",
            file_name="Program.cs",
            coverable_lines=100,
            covered_lines=50,
            uncovered_line_numbers=[10, 11, 13, 15, 17],
            branches=25,
            covered_branches=10,
        )
    ]

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered  |  Uncovered Lines
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Program     |              100  |             50  |        25  |                10  |  10-11, 13...   
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        """

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)


def test_format_coverage_items_when_n0_uncovered_lines_exist_for_file_returns_formatted_string():
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

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered  |  Uncovered Lines
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        Program     |              100  |             50  |        25  |                10  |                 
        ------------|-------------------|-----------------|------------|--------------------|-------------------
        """

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)
