# ====================================================================
# NEUROSONIC TRINITY+ASI - STARTUP LAUNCHER (PWSH POPUP)
# Hap 3 dritare popup me pwsh: Lightning SPP, Backend, Frontend.
# ====================================================================

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC TRINITY+ASI STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PwshExe = (Get-Command pwsh -ErrorAction Stop).Source

$LightningPopup = Join-Path $ProjectRoot "scripts\popup_lightning.ps1"
$BackendPopup = Join-Path $ProjectRoot "scripts\popup_backend.ps1"
$FrontendPopup = Join-Path $ProjectRoot "scripts\popup_frontend.ps1"

foreach ($ScriptPath in @($LightningPopup, $BackendPopup, $FrontendPopup)) {
    if (-not (Test-Path $ScriptPath)) {
        throw "Popup script nuk u gjet: $ScriptPath"
    }
}

Write-Host "[1/3] Duke hapur popup per Lightning SPP..." -ForegroundColor Yellow
Start-Process -FilePath $PwshExe -ArgumentList @("-NoExit", "-File", $LightningPopup) -WorkingDirectory $ProjectRoot
Start-Sleep -Seconds 2

Write-Host "[2/3] Duke hapur popup per Backend API..." -ForegroundColor Yellow
Start-Process -FilePath $PwshExe -ArgumentList @("-NoExit", "-File", $BackendPopup) -WorkingDirectory $ProjectRoot
Start-Sleep -Seconds 2

Write-Host "[3/3] Duke hapur popup per Frontend..." -ForegroundColor Yellow
Start-Process -FilePath $PwshExe -ArgumentList @("-NoExit", "-File", $FrontendPopup) -WorkingDirectory $ProjectRoot

if ($env:NEUROSONIC_NO_BROWSER -ne "1") {
    Start-Sleep -Seconds 2
    Write-Host "Duke hapur dashboard ne browser..." -ForegroundColor DarkGray
    Start-Process "http://localhost:8000/neurosonic_dashboard.html"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 POPUP 1/2/3 U NISEN ME PWSH" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Lightning SPP: http://localhost:8080" -ForegroundColor Cyan
Write-Host "  Backend API:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Frontend:      http://localhost:5500" -ForegroundColor Cyan
Write-Host "  Dashboard API/Ops: http://localhost:8000/dashboard" -ForegroundColor Cyan
Write-Host "  Dashboard DNA UI:  http://localhost:8000/dna-ui" -ForegroundColor Cyan
Write-Host "  Frontend Dashboard: http://localhost:5500/neurosonic_dashboard.html" -ForegroundColor DarkGray
Write-Host ""

