$rootDir = (get-item $PSScriptRoot).Parent.FullName

pyinstaller "$rootDir/cobertura_console_reporter/__main__.py" --name ccr --onefile
