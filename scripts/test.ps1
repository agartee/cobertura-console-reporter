$rootDir = (get-item $PSScriptRoot).Parent.FullName
$testsPath = "$($rootDir)\tests"

Write-Host "Tests:" -ForegroundColor Blue
Write-Host ""

coverage run -m pytest $testsPath -v --no-header --capture=no
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Test Coverage:" -ForegroundColor Blue
Write-Host ""

coverage report -m

Write-Host ""
Write-Host "Linting:" -ForegroundColor Blue

pylint "$($rootDir)\cobertura_console_reporter"
