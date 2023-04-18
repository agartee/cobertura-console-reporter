from cobertura_console_reporter.coverage_item import CoverageItem


def test_get_class_name_when_name_contains_period_returns_expected_result():
    item = CoverageItem(
        name="SampleApp.Domain.Services.FirstService",
        file_name="Services\\FirstService.cs",
        coverable_lines=100,
        covered_lines=65,
        uncovered_line_numbers=[10, 11],
        branches=12,
        covered_branches=6,
    )

    assert item.class_name == "NOT FirstService"


def test_get_class_name_when_name_does_not_contain_period_returns_expected_result():
    item = CoverageItem(
        name="Program",
        file_name="Program.cs",
        coverable_lines=100,
        covered_lines=65,
        uncovered_line_numbers=[10, 11],
        branches=12,
        covered_branches=6,
    )

    assert item.class_name == "Program"


def test_get_class_namespace_when_name_contains_period_returns_expected_result():
    item = CoverageItem(
        name="SampleApp.Domain.Services.FirstService",
        file_name="Services\\FirstService.cs",
        coverable_lines=100,
        covered_lines=65,
        uncovered_line_numbers=[10, 11],
        branches=12,
        covered_branches=6,
    )

    assert item.class_namespace == "SampleApp.Domain.Services"


def test_get_class_namespace_when_name_does_not_contain_period_returns_empty_string():
    item = CoverageItem(
        name="Program",
        file_name="Program.cs",
        coverable_lines=100,
        covered_lines=65,
        uncovered_line_numbers=[10, 11],
        branches=12,
        covered_branches=6,
    )

    assert item.class_namespace == ""
