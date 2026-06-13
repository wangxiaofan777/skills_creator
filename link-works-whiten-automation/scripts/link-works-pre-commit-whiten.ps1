<#
.SYNOPSIS
  git pre-commit hook: whiten staged files that still have Link Works manualLine > 0.
#>
$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $RepoRoot) {
    Write-Error 'Must run inside a git repository.'
    exit 1
}
Set-Location $RepoRoot

$StatsScript = Join-Path $ScriptDir 'lib/link-works-stats.mjs'
$statsJson = & node $StatsScript list-staged-pending 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error $statsJson
    Write-Host 'Link Works pre-commit whitening failed. Open Cursor on this repo and run scripts/link-works-whiten-all.ps1, or use git commit --no-verify to skip.' -ForegroundColor Yellow
    exit 1
}

$stats = $statsJson | ConvertFrom-Json
$pending = @($stats.pending)
if ($pending.Count -eq 0) {
    exit 0
}

Write-Host "Link Works pre-commit: whitening $($pending.Count) staged file(s)..."
foreach ($entry in $pending) {
    Write-Host ("  {0}" -f $entry.absolutePath)
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
$payloadPath = Join-Path $payloadDir 'pre-commit-run-commands.json'
$commands | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $payloadPath -Encoding UTF8

$invokeScript = Join-Path $ScriptDir 'link-works-invoke-run-commands.ps1'
& $invokeScript -PayloadPath $payloadPath
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Link Works auto-whiten could not reach Cursor. Keep Cursor open and retry, or git commit --no-verify.' -ForegroundColor Yellow
    exit 1
}

Write-Host 'Dispatched whitening commands. Verify Link Works panel shows otherLine=0, then commit again if needed.'
exit 0
