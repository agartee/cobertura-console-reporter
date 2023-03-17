import textwrap

from cobertura_parser.coverage_item import CoverageItem
from cobertura_parser.formatter import format_coverage_items



def test_format_coverage_items_returns_formatted_string():
    items = [
        CoverageItem("SampleApp.Domain.Services.FirstService", "Services\FirstService.cs", 100, 65, 12, 6),
        CoverageItem("SampleApp.Domain.Services.SecondService", "Services\SecondService.cs", 100, 65, 12, 6)
    ]

    expected = '''\
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        Class Name                               |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        SampleApp.Domain.Services.FirstService   |               65  |              6  |        12  |               100
        SampleApp.Domain.Services.SecondService  |               65  |              6  |        12  |               100
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        '''

    result = format_coverage_items(items)

    assert result == textwrap.dedent(expected)
