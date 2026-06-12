# One-time: point SONARGUARD_HOME at your skills_creator clone (any path).
param(
    [string]$PackageRoot
)

$ErrorActionPreference = "Stop"
$installRel = "sonar-guard\scripts\install.py"

function Test-PackageRoot([string]$Path) {
    return (Test-Path (Join-Path $Path $installRel))
}

if (-not $PackageRoot) {
    $PackageRoot = Read-Host "skills_creator clone path (where sonar-guard/scripts/install.py lives)"
}
$PackageRoot = (Resolve-Path $PackageRoot).Path

if (-not (Test-PackageRoot $PackageRoot)) {
    Write-Error "Invalid path: missing $installRel under $PackageRoot"
}

$configDir = Join-Path $env:USERPROFILE ".config\sonarguard"
$configFile = Join-Path $configDir "config.json"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

$data = @{}
if (Test-Path $configFile) {
    try { $data = Get-Content $configFile -Raw | ConvertFrom-Json -AsHashtable } catch { $data = @{} }
}
$data["packageRoot"] = $PackageRoot
$data | ConvertTo-Json | Set-Content -Path $configFile -Encoding UTF8

[Environment]::SetEnvironmentVariable("SONARGUARD_HOME", $PackageRoot, "User")
$env:SONARGUARD_HOME = $PackageRoot

Write-Host "OK: packageRoot -> $PackageRoot"
Write-Host "OK: SONARGUARD_HOME set (User). Open a new terminal, then from business repo:"
Write-Host '  python "$env:SONARGUARD_HOME/sonar-guard/scripts/install_bootstrap.py" --platform all --repo .'
