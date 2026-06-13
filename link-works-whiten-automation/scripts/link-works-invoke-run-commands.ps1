<#
.SYNOPSIS
  Invoke VS Code/Cursor runCommands for Link Works whitening.

.DESCRIPTION
  Cursor CLI (3.x) does not expose a direct runCommands subcommand. This script
  opens vscode://vscode.runCommands?data=... which Cursor registers as a handler
  when the IDE is running. Use -DryRun to print the URI without launching.

.PARAMETER CommandsJson
  JSON array of { "command": "...", "args": [...] } objects.

.PARAMETER PayloadPath
  Path to a JSON file containing the commands array.

.PARAMETER DryRun
  Print payload and URI only; do not invoke.
#>
param(
    [string] $CommandsJson,
    [string] $PayloadPath,
    [switch] $DryRun
)

$ErrorActionPreference = 'Stop'

function Get-CommandsArray {
    param([string] $Json, [string] $Path)
    if ($Path) {
        if (-not (Test-Path -LiteralPath $Path)) {
            throw "Payload file not found: $Path"
        }
        $Json = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    }
    if ([string]::IsNullOrWhiteSpace($Json)) {
        throw 'Provide -CommandsJson or -PayloadPath.'
    }
    $parsed = $Json | ConvertFrom-Json
    if (-not ($parsed -is [System.Array])) {
        throw 'Commands payload must be a JSON array.'
    }
    return ,$parsed
}

function ConvertTo-RunCommandsUri {
    param($Commands)
    $compact = $Commands | ConvertTo-Json -Compress -Depth 20
    $encoded = [uri]::EscapeDataString($compact)
    return "vscode://vscode.runCommands?data=$encoded"
}

try {
    $commands = Get-CommandsArray -Json $CommandsJson -Path $PayloadPath
    if ($commands.Count -eq 0) {
        Write-Host 'No commands to run.'
        exit 0
    }

    $uri = ConvertTo-RunCommandsUri -Commands $commands
    Write-Host "runCommands entries: $($commands.Count)"
    if ($DryRun) {
        Write-Host "URI: $uri"
        exit 0
    }

    Start-Process -FilePath $uri | Out-Null
    Write-Host 'Dispatched vscode://vscode.runCommands (Cursor must be running with this repo open).'
    exit 0
}
catch {
    Write-Error $_
    Write-Host @"

Failed to dispatch runCommands via URI.
Fallback:
  1. Keep Cursor open on this repository.
  2. Command Palette -> Tasks: Run Task -> Link Works: Whiten All Pending
  3. Or run scripts/link-works-whiten-all.ps1 again after confirming Cursor is running.

"@ -ForegroundColor Yellow
    exit 1
}
