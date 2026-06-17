param([string]$Notes = "content update")
# Bump version across version.json / sw.js(BUILD_VERSION) / index.html(APP_VERSION). Writes UTF-8 no BOM.
# NOTE: keep this script ASCII-only -- Windows PowerShell 5.1 parses no-BOM .ps1 as the system (Big5) codepage,
#       so non-ASCII characters here (esp. full-width brackets) break string parsing.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$enc  = New-Object System.Text.UTF8Encoding($false)
$today = Get-Date -Format "yyyy.MM.dd"
$vp = Join-Path $root "version.json"; $seq = 1
if (Test-Path $vp) {
  $old = (Get-Content $vp -Encoding UTF8 -Raw | ConvertFrom-Json).version
  if ($old -match "^$([regex]::Escape($today))-(\d+)$") { $seq = [int]$Matches[1] + 1 }
}
$ver = "$today-$seq"
[System.IO.File]::WriteAllText($vp, ([ordered]@{version=$ver; notes=$Notes} | ConvertTo-Json), $enc)
foreach ($f in @(@("sw.js","const BUILD_VERSION = '[^']*';","const BUILD_VERSION = '$ver';"),
                 @("index.html","var APP_VERSION='[^']*';","var APP_VERSION='$ver';"),
                 @("index.html", 'assets/og-cover.png\?v=[^"'']*', "assets/og-cover.png?v=$ver"))) {
  $p = Join-Path $root $f[0]; $t = [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8)
  [System.IO.File]::WriteAllText($p, [regex]::Replace($t, $f[1], $f[2]), $enc)
}
Write-Host "bumped -> $ver  (next: git add -A; git commit; git push)"
