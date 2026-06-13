<#
.SYNOPSIS
  Batch-whiten all Link Works files with manualLine > 0 in the current repo.

.PARAMETER DryRun
  List pending files and print runCommands payload without invoking.

.PARAMETER ListOnly
  Print pending JSON from link-works-stats.mjs and exit.
#>
param(
    [switch] $DryRun,
    [switch] $ListOnly
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $RepoRoot) {
    Write-Error 'Must run inside a git repository.'
    exit 1
}
Set-Location $RepoRoot

$StatsScript = Join-Path $ScriptDir 'lib/link-works-stats.mjs'
if (-not (Test-Path -LiteralPath $StatsScript)) {
    Write-Error "Missing $StatsScript"
    exit 1
}

$statsJson = & node $StatsScript list-pending 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error $statsJson
    exit 1
}

$stats = $statsJson | ConvertFrom-Json
$pending = @($stats.pending)
if ($pending.Count -eq 0) {
    Write-Host 'No Link Works whitening needed (all manualLine are 0).'
    exit 0
}

Write-Host "Pending whitening: $($pending.Count) file(s)."
foreach ($entry in $pending) {
    Write-Host ("  {0} manualLine={1}" -f $entry.absolutePath, $entry.manualLine)
}

if ($ListOnly) {
    exit 0
}

$commands = @()
foreach ($entry in $pending) {
    $commands += [ordered]@{
        command = 'link-works.whiteningFile'
        args    = @($entry.absolutePath)
    }
}

$payloadDir = Join-Path $env:TEMP 'link-works-whiten'
New-Item -ItemType Directory -Force -Path $payloadDir | Out-Null
$payloadPath = Join-Path $payloadDir 'run-commands.json'
$commands | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $payloadPath -Encoding UTF8

$invokeScript = Join-Path $ScriptDir 'link-works-invoke-run-commands.ps1'
$invokeArgs = @{
    PayloadPath = $payloadPath
}
if ($DryRun) {
    $invokeArgs['DryRun'] = $true
}

& $invokeScript @invokeArgs
exit $LASTEXITCODE
