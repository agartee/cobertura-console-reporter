from cobertura_reporter.coverage_item import CoverageItem


def test_get_class_name_returns_expected_result():
    item = CoverageItem("SampleApp.Domain.Services.FirstService", 
                        "Services\FirstService.cs", 100, 65, 12, 6)
    
    assert item.class_name == "FirstService"



def test_get_class_namespace_returns_expected_result():
    item = CoverageItem("SampleApp.Domain.Services.FirstService", 
                        "Services\FirstService.cs", 100, 65, 12, 6)
    
    assert item.class_namespace == "SampleApp.Domain.Services"
