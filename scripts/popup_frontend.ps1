# ====================================================================
# NEUROSONIC FRONTEND STARTUP
# Hap nje dritare te re PowerShell per Frontend Server
# ====================================================================

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$port = 5500

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC FRONTEND - Duke u nisur..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend Server: http://localhost:$port" -ForegroundColor Green
Write-Host "Dashboard:       http://localhost:$port/neurosonic_dashboard.html" -ForegroundColor Green
Write-Host ""

# Shko ne projekt
Set-Location $ProjectRoot

# Nise Python HTTP server per frontend
Write-Host "🚀 Duke nisur Frontend Server..." -ForegroundColor Green
python -m http.server $port --bind 0.0.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Gabim! Frontend server nuk u nis." -ForegroundColor Red
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
}

