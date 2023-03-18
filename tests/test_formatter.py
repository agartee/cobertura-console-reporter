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
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        Class Name                               |  Lines Coverable  |  Lines Covered  |  Branches  |  Branches Covered
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        SampleApp.Domain.Services.FirstService   |              100  |             65  |        12  |                 6
        SampleApp.Domain.Services.SecondService  |              100  |             65  |        12  |                 6
        -----------------------------------------|-------------------|-----------------|------------|--------------------
        '''

    result = format_coverage_items(items, colorize=False)

    assert result == textwrap.dedent(expected)
