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

$existingListener = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue |
Select-Object -First 1
if ($existingListener) {
    $processInfo = Get-Process -Id $existingListener.OwningProcess -ErrorAction SilentlyContinue
    if ($processInfo) {
        Write-Host ("❌ Porta 8080 eshte e zene nga {0} (PID {1})." -f $processInfo.ProcessName, $processInfo.Id) -ForegroundColor Red
    }
    else {
        Write-Host ("❌ Porta 8080 eshte e zene nga PID {0}." -f $existingListener.OwningProcess) -ForegroundColor Red
    }
    Write-Host "Mbyll instancen ekzistuese ose perdor start_neurosonic.ps1 per auto-clean." -ForegroundColor Yellow
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
    exit 1
}

Write-Host "🚀 Duke nisur Lightning SPP..." -ForegroundColor Green
$env:PYTHONUTF8 = "1"
& $PythonExe -u $LightningEntry

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Gabim! Lightning SPP nuk u nis." -ForegroundColor Red
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
}
