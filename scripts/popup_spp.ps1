# ====================================================================
# NEUROSONIC LIGHTNING SPP STARTUP
# ====================================================================

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SppScript = Join-Path $ProjectRoot "repos\Lightning-SPP-3.14\lightning_spp_server.py"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIGHTNING SPP 3.14 - Duke u nisur..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path $VenvPython) {
    $PythonExe = $VenvPython
} else {
    $PythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
Set-Location $ProjectRoot
& $PythonExe -u $SppScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "[GABIM] Lightning SPP nuk u nis (exit code $LASTEXITCODE)." -ForegroundColor Red
    Read-Host "Shtyp ENTER per ta mbyllur"
}
