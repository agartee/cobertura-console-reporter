$rootDir = (get-item $PSScriptRoot).Parent.FullName
$testsPath = "$($rootDir)\tests"

pytest $testsPath
