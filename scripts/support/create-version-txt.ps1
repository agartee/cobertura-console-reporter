param(
  [Parameter(Mandatory = $true)]
  [Alias("v")]
  [string]$Version,

  # Optional: where to write the file (defaults to ./version.txt)
  [string]$OutFile = (Join-Path (Get-Location) "version.txt")
)

$ErrorActionPreference = "Stop"

# Strip leading v/V (only if it's the first character)
$ver = $Version.Trim()
if ($ver.Length -gt 0 -and ($ver[0] -eq 'v' -or $ver[0] -eq 'V')) {
  $ver = $ver.Substring(1)
}

# Expect semantic-ish "MAJOR.MINOR.PATCH" (PATCH can be missing; defaults to 0)
$parts = $ver.Split('.')
if ($parts.Count -lt 2 -or $parts.Count -gt 4) {
  throw "Version must be like '1.2.3' (or 'v1.2.3'). Got: '$Version'"
}

$maj = [int]$parts[0]
$min = [int]$parts[1]
$pat = if ($parts.Count -ge 3 -and $parts[2] -ne "") { [int]$parts[2] } else { 0 }
$bld = if ($parts.Count -ge 4 -and $parts[3] -ne "") { [int]$parts[3] } else { 0 }

$dir = Split-Path -Parent $OutFile
if ($dir -and -not (Test-Path $dir)) {
  New-Item -ItemType Directory -Path $dir | Out-Null
}

@"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=($maj, $min, $pat, $bld),
    prodvers=($maj, $min, $pat, $bld),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [
          StringStruct(u'CompanyName', u'Adam Gartee'),
          StringStruct(u'FileDescription', u'Cobertura console reporter'),
          StringStruct(u'FileVersion', u'$ver'),
          StringStruct(u'LegalCopyright', u'Copyright (c) $((Get-Date).Year) Adam Gartee'),
          StringStruct(u'ProductName', u'cobertura-console-reporter'),
          StringStruct(u'ProductVersion', u'$ver'),
          StringStruct(u'OriginalFilename', u'ccr.exe')
        ]
      )
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"@ | Set-Content -Encoding utf8 -NoNewline $OutFile

Write-Host "Wrote version file: $OutFile"
Write-Host "Version: $ver (filevers/prodvers = $maj.$min.$pat.$bld)"
