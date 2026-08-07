[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
$source = $PSScriptRoot
$root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$gitDir = (& git -C $root rev-parse --git-path hooks).Trim()
if (-not [System.IO.Path]::IsPathRooted($gitDir)) {
    $gitDir = Join-Path $root $gitDir
}
New-Item -ItemType Directory -Force -Path $gitDir | Out-Null
foreach ($hook in @('pre-commit', 'pre-push')) {
    Copy-Item -LiteralPath (Join-Path $source $hook) -Destination (Join-Path $gitDir $hook) -Force
}
Write-Host "Installed documentation-governance hooks for Windows and Unix-compatible Git at $gitDir"
