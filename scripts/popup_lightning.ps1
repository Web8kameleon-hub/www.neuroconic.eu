# ====================================================================
# NEUROSONIC LIGHTNING SPP STARTUP
# Hap nje dritare te re pwsh per Lightning SPP server
# ====================================================================

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = (Get-Command python -ErrorAction Stop).Source
}

$LightningEntry = Join-Path $ProjectRoot "repos\Lightning-SPP-3.14\lightning_spp_server.py"
if (-not (Test-Path $LightningEntry)) {
    throw "Lightning SPP entrypoint nuk u gjet: $LightningEntry"
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC LIGHTNING SPP - Duke u nisur..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lightning SPP: http://localhost:8080" -ForegroundColor Green
Write-Host ""

Set-Location $ProjectRoot

Write-Host "🚀 Duke nisur Lightning SPP..." -ForegroundColor Green
& $PythonExe -u $LightningEntry

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Gabim! Lightning SPP nuk u nis." -ForegroundColor Red
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
}
