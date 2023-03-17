from cobertura_parser import parser


def test_parse_returns_correct_number_of_results():
    results = parser.parse("sample_data/coverage.cobertura.xml")
    assert len(results) == 2  

def test_parse_return_results_with_class_name():
    results = parser.parse("sample_data/coverage.cobertura.xml")
        
    assert any('SampleApp.Domain.Services.SomeService' in r.name for r in results) 
    assert any('SampleApp.Domain.Services.StringExtensions' in r.name for r in results) 
    
def test_parse_return_results_with_file_name():
    results = parser.parse("sample_data/coverage.cobertura.xml")
    
    assert all('Services\\SomeService.cs' in r.file_name for r in results) 

def test_parse_return_results_with_coverable_lines():
    results = iter(parser.parse("sample_data/coverage.cobertura.xml"))
    
    assert next(iter([
        r.coverable_lines for r in results 
        if r.name == 'SampleApp.Domain.Services.SomeService'
        ])) == 32

def test_parse_return_results_with_covered_lines():
    results = iter(parser.parse("sample_data/coverage.cobertura.xml"))
    
    assert next(iter([
        r.covered_lines for r in results 
        if r.name == 'SampleApp.Domain.Services.SomeService'
        ])) == 31
    
def test_parse_return_results_with_branches():
    results = iter(parser.parse("sample_data/coverage.cobertura.xml"))
    
    assert next(iter([
        r.branches for r in results 
        if r.name == 'SampleApp.Domain.Services.SomeService'
        ])) == 12

def test_parse_return_results_with_covered_branches():
    results = iter(parser.parse("sample_data/coverage.cobertura.xml"))
    
    assert next(iter([
        r.covered_branches for r in results 
        if r.name == 'SampleApp.Domain.Services.SomeService'
        ])) == 9
