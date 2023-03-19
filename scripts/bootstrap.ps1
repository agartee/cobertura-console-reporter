$rootDir = (get-item $PSScriptRoot).Parent.FullName

# **************************************************************************************
# Check Python Installation
# **************************************************************************************
$minPythonVersion = "3.9.6"
try {
    # note: capture the "out" and "error" messages, but do not print them
    Invoke-Expression "python --version" `
        -ErrorVariable errOut -OutVariable succOut 2>&1 | Out-Null
    
    if (-not $succOut) {
        throw [System.InvalidOperationException] `
            "Python installation not found (minimum: $($minPythonVersion))."
    }

    $currentPythonVer = $succOut.Replace("Python ", "")
    if ([System.Version] $currentPythonVer -lt [System.Version] $minPythonVersion) {
        throw [System.InvalidOperationException] `
        ("Current Python version not supported (found: $($currentPythonVer);" `
                + " minimum: $($minPythonVersion)).")
    }

    Write-Host ("Python installation found: $($currentPythonVer) (minimum:" `
            + "$($minPythonVersion)).") -ForegroundColor Green
}
catch [System.Exception] {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit
}

# **************************************************************************************
# Create and Activate Python Virtual Environment
# **************************************************************************************
$venvPath = "$($rootDir)\.venv"

if (Test-Path -Path $venvPath) {
    Write-Host "Python virtual environment detected." -ForegroundColor Green
}
else {
    python -m venv $venvPath
    Write-Host "Python virtual environment created." -ForegroundColor Green
}

Invoke-Expression ". ""$($venvPath)\Scripts\Activate.ps1"""
Write-Host "Python virtual environment activated." -ForegroundColor Green

# **************************************************************************************
# Install Python Development Dependencies
# **************************************************************************************
python -m pip install --upgrade pip 2>&1 | Out-Null
pip install -r "$($rootDir)\requirements-dev.txt" 2>&1 | Out-Null

Write-Host "Python development dependencies installed." -ForegroundColor Green
