$rootDir = (get-item $PSScriptRoot).Parent.FullName

# **************************************************************************************
# Delete Python Virtual Environment (if exists)
# **************************************************************************************
$venvPath = "$($rootDir)\.venv"

if (Test-Path -Path $venvPath) {
    Remove-Item -Recurse -Force "$($rootDir)\.venv"
    Write-Host "Python virtual environment deleted." -ForegroundColor Green
}

# **************************************************************************************
# Bootstrap
# **************************************************************************************
& "$($rootDir)\scripts\bootstrap.ps1"
