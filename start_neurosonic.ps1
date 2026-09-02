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

$PortsToFree = @(8080, 8000, 5500)
Write-Host "[0/3] Duke pastruar instancat e vjetra ne porta 8080/8000/5500..." -ForegroundColor DarkYellow
foreach ($Port in $PortsToFree) {
    $ProcessIds = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($ProcessId in $ProcessIds) {
        try {
            Stop-Process -Id $ProcessId -Force -ErrorAction Stop
            Write-Host ("  ✅ Porta {0} u lirua (PID {1})" -f $Port, $ProcessId) -ForegroundColor DarkGray
        }
        catch {
            Write-Host ("  ⚠️ Nuk u ndal PID {0} ne porten {1}: {2}" -f $ProcessId, $Port, $_.Exception.Message) -ForegroundColor Yellow
        }
    }
}
Start-Sleep -Milliseconds 800

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

