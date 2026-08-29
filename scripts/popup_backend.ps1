# ====================================================================
# NEUROSONIC BACKEND STARTUP
# Hap nje dritare te re PowerShell per Backend API
# ====================================================================

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

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
$env:PYTHONUTF8 = "1"

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $PythonExe = $VenvPython
} else {
    $PythonExe = (Get-Command python -ErrorAction Stop).Source
}

# Kontrollo nese fastapi eshte i instaluar
$fastapiCheck = & $PythonExe -c "import fastapi" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[SETUP] Instaloj dependencies..." -ForegroundColor Yellow
    & $PythonExe -m pip install fastapi uvicorn pydantic
}

# Nise backend-in
Write-Host "[START] Duke nisur Neurosonic Backend API..." -ForegroundColor Green
& $PythonExe -u backend/main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[GABIM] Backend API nuk u nis." -ForegroundColor Red
    Write-Host "Shtypni ENTER per te mbyllur..." -ForegroundColor Yellow
    Read-Host
}

