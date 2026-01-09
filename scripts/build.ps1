param(
    [Parameter(Mandatory = $true)]
    [Alias("v")]
    [string]$Version
)

$ErrorActionPreference = "Stop"
$rootDir = (get-item $PSScriptRoot).Parent.FullName

& "$rootDir/scripts/support/create-version-txt.ps1" -Version $Version -OutFile "$rootDir/build/version.txt"
pyinstaller "$rootDir/cobertura_console_reporter/__main__.py" --name ccr --onefile --version-file "$rootDir/build/version.txt"
