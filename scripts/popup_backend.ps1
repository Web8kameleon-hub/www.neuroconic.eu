# ====================================================================
# NEUROSONIC BACKEND STARTUP
# Hap nje dritare te re PowerShell per Backend API
# ====================================================================

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = (Get-Command python -ErrorAction Stop).Source
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC BACKEND API - Duke u nisur..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "FastAPI Server: http://localhost:8000" -ForegroundColor Green
Write-Host "Swagger Docs:   http://localhost:8000/docs" -ForegroundColor Green
Write-Host "ReDoc Docs:     http://localhost:8000/redoc" -ForegroundColor Green
Write-Host ""

# Shko ne projekt
Set-Location $ProjectRoot

# Kontrollo nese fastapi eshte i instaluar
$fastapiCheck = & $PythonExe -c "import fastapi" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Instaloj dependencies..." -ForegroundColor Yellow
    & $PythonExe -m pip install fastapi uvicorn pydantic
}

# Nise backend-in
Write-Host "🚀 Duke nisur Neurosonic Backend API..." -ForegroundColor Green
$env:PYTHONUTF8 = "1"
& $PythonExe backend/main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Gabim! Backend API nuk u nis." -ForegroundColor Red
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
}

