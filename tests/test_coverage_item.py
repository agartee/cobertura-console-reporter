from cobertura_console_reporter.coverage_item import CoverageItem


def test_get_class_name_when_name_contains_period_returns_expected_result():
    item = CoverageItem("SampleApp.Domain.Services.FirstService", 
                        "Services\FirstService.cs", 100, 65, 12, 6)
    
    assert item.class_name == "FirstService"

def test_get_class_name_when_name_does_not_contain_period_returns_expected_result():
    item = CoverageItem("Program", "Program.cs", 100, 65, 12, 6)
    
    assert item.class_name == "Program"

def test_get_class_namespace_when_name_contains_period_returns_expected_result():
    item = CoverageItem("SampleApp.Domain.Services.FirstService", 
                        "Services\FirstService.cs", 100, 65, 12, 6)
    
    assert item.class_namespace == "SampleApp.Domain.Services"

def test_get_class_namespace_when_name_does_not_contain_period_returns_empty_string():
    item = CoverageItem("Program", "Program.cs", 100, 65, 12, 6)
    
    assert item.class_namespace == ""
