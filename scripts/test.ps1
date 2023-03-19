$rootDir = (get-item $PSScriptRoot).Parent.FullName
$testsPath = "$($rootDir)\tests"

coverage run -m pytest $testsPath -v --no-header --capture=no

Write-Host ""
Write-Host "Test coverage report" -ForegroundColor Blue
Write-Host ""

coverage report -m
