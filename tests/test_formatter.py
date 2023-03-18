import textwrap

from cobertura_reporter.coverage_item import CoverageItem
from cobertura_reporter.formatter import format_coverage_items


def test_format_coverage_items_returns_formatted_string():
    items = [
        CoverageItem("SampleApp.Domain.Services.FirstService", 
                     "Services\FirstService.cs", 100, 65, 12, 6),
        CoverageItem("SampleApp.Domain.Services.SecondService", 
                     "Services\SecondService.cs", 100, 65, 12, 6)
    ]

    expected = '''\
        ---------------------------|-------------------|-----------------|------------|--------------------
        Class Name                 |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ---------------------------|-------------------|-----------------|------------|--------------------
        SampleApp.Domain.Services  |              200  |            130  |        24  |                12
          FirstService             |              100  |             65  |        12  |                 6
          SecondService            |              100  |             65  |        12  |                 6
        ---------------------------|-------------------|-----------------|------------|--------------------
        '''

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)

def test_format_coverage_items_when_namespace_and_class_names_shorter_than_header_returns_formatted_string():
    items = [
        CoverageItem("A.B.C", 
                     "C.cs", 100, 50, 25, 10)
    ]

    expected = '''\
        ------------|-------------------|-----------------|------------|--------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ------------|-------------------|-----------------|------------|--------------------
        A.B         |              100  |             50  |        25  |                10
          C         |              100  |             50  |        25  |                10
        ------------|-------------------|-----------------|------------|--------------------
        '''

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)

def test_format_coverage_items_when_class_does_not_have_namespace_returns_formatted_string():
    items = [
        CoverageItem("Program", 
                     "Program.cs", 100, 50, 25, 10)
    ]

    expected = '''\
        ------------|-------------------|-----------------|------------|--------------------
        Class Name  |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        ------------|-------------------|-----------------|------------|--------------------
        Program     |              100  |             50  |        25  |                10
        ------------|-------------------|-----------------|------------|--------------------
        '''

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)
