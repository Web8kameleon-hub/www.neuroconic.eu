# ====================================================================
# NEUROSONIC TRINITY+ASI - STARTUP LAUNCHER
# Hap 3 dritare PowerShell: Backend, Frontend, dhe hap browser-in
# ====================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC TRINITY+ASI STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendScript = Join-Path $ProjectRoot "scripts\popup_backend.ps1"
$FrontendScript = Join-Path $ProjectRoot "scripts\popup_frontend.ps1"
$SppLauncher = Join-Path $ProjectRoot "scripts\popup_spp.ps1"
$DashboardUrl = "http://localhost:5500/neurosonic_dashboard.html"

# Hap dritare per Lightning SPP (port 8080) - Sherben Scan/Process/Print
Write-Host "[1/4] Duke nisur Lightning SPP 3.14..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $SppLauncher

$sppReady = $false
for ($attempt = 1; $attempt -le 10; $attempt++) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 1
        if ($response.status -eq "healthy") {
            $sppReady = $true
            break
        }
    } catch { }
}
if (-not $sppReady) {
    Write-Host "[GABIM] Lightning SPP nuk u hap ne porten 8080. Shiko dritaren e tij." -ForegroundColor Red
}

# Hap dritare per Backend
Write-Host "[2/4] Duke hapur Backend API..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '$BackendScript'"

Start-Sleep -Seconds 2

# Hap dritare per Frontend
Write-Host "[3/4] Duke hapur Frontend Server..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '$FrontendScript'"

Start-Sleep -Seconds 3

# Hap browser
Write-Host "[4/4] Duke hapur Dashboard ne browser..." -ForegroundColor Yellow
Start-Process $DashboardUrl

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 NEUROSONIC ESHTE DUKE EKZEKUTUAR!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Lightning SPP: http://localhost:8080" -ForegroundColor Cyan
Write-Host "  Backend API:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs:      http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Frontend:      http://localhost:5500" -ForegroundColor Cyan
Write-Host "  Dashboard:     http://localhost:5500/neurosonic_dashboard.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ⚠️  MOS MBYLLNI DRITARET E POWERSHELL!" -ForegroundColor Red
Write-Host "     Ato sherbejne Lightning SPP, Backend dhe Frontend." -ForegroundColor Red
Write-Host ""

# Mbaj skriptin hapur
Read-Host "Shtypni ENTER per te mbyllur kete dritare"

