$rootDir = (get-item $PSScriptRoot).Parent.FullName
$testsPath = "$($rootDir)\tests"

coverage run -m pytest $testsPath -v --no-header --capture=no

Write-Host ""
Write-Host "Test Coverage:" -ForegroundColor Blue
Write-Host ""

coverage report -m

Write-Host ""
Write-Host "Linting:" -ForegroundColor Blue

pylint "$($rootDir)\cobertura_console_reporter"
