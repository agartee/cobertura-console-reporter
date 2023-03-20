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
            branches=12,
            covered_branches=6,
        ),
        CoverageItem(
            name="SampleApp.Domain.Services.SecondService",
            file_name="Services\\SecondService.cs",
            coverable_lines=100,
            covered_lines=65,
            branches=12,
            covered_branches=6,
        ),
    ]

    expected = """\
        ---------------------------|-------------------|-----------------|------------|--------------------
        Class Name                 |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ---------------------------|-------------------|-----------------|------------|--------------------
        SampleApp.Domain.Services  |              200  |            130  |        24  |                12
          FirstService             |              100  |             65  |        12  |                 6
          SecondService            |              100  |             65  |        12  |                 6
        ---------------------------|-------------------|-----------------|------------|--------------------
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
            branches=25,
            covered_branches=10,
        )
    ]

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ------------|-------------------|-----------------|------------|--------------------
        A.B         |              100  |             50  |        25  |                10
          C         |              100  |             50  |        25  |                10
        ------------|-------------------|-----------------|------------|--------------------
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
            branches=25,
            covered_branches=10,
        )
    ]

    expected = """\
        ------------|-------------------|-----------------|------------|--------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ------------|-------------------|-----------------|------------|--------------------
        Program     |              100  |             50  |        25  |                10
        ------------|-------------------|-----------------|------------|--------------------
        """

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)
