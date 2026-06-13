<#
.SYNOPSIS
  Opt-in installer for Link Works pre-commit whitening hook.

.PARAMETER SkipHook
  Print paths only; do not modify .git/hooks/pre-commit.
#>
param(
    [switch] $SkipHook
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $RepoRoot) {
    Write-Error 'Must run inside a git repository.'
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HookScript = Join-Path $ScriptDir 'link-works-pre-commit-whiten.ps1'
$HookScriptPosix = $HookScript -replace '\\', '/'
$Marker = '# link-works-batch-whiten-automation'
$HookPath = Join-Path $RepoRoot '.git/hooks/pre-commit'

$hookBody = @"
#!/bin/sh
$Marker
"$HookScriptPosix"
status=`$?
if [ `$status -ne 0 ]; then
  exit `$status
fi
"@

if ($SkipHook) {
    Write-Host "Would install hook at: $HookPath"
    Write-Host $hookBody
    exit 0
}

if (Test-Path -LiteralPath $HookPath) {
    $existing = Get-Content -LiteralPath $HookPath -Raw -Encoding UTF8
    if ($existing -match [regex]::Escape($Marker)) {
        Write-Host 'Link Works pre-commit hook already installed.'
        exit 0
    }
    $backup = "$HookPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -LiteralPath $HookPath -Destination $backup -Force
    Write-Host "Backed up existing pre-commit hook to $backup"
    $merged = @"
$existing

$hookBody
"@
    Set-Content -LiteralPath $HookPath -Value $merged -Encoding UTF8 -NoNewline
}
else {
    Set-Content -LiteralPath $HookPath -Value $hookBody -Encoding UTF8 -NoNewline
}

if ($IsWindows -or $env:OS -match 'Windows') {
    # Git for Windows runs hooks via sh; no chmod required on NTFS for core.hooksPath default.
}

Write-Host "Installed Link Works pre-commit hook: $HookPath"
Write-Host 'Requires Cursor running with this repo open when committing staged files with manualLine > 0.'
