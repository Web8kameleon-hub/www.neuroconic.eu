# ====================================================================
# NEUROSONIC - ROLLING UPDATE FOR BACKEND
# Recreate backend and validate health via Nginx.
# ====================================================================

param(
    [string]$ComposeFile = (Join-Path (Split-Path -Parent $PSScriptRoot) "docker-compose.yml"),
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$HealthUrl = "https://127.0.0.1/api/health",
    [string]$ThinkUrl = "https://127.0.0.1/api/shell/think",
    [int]$HealthTimeoutSeconds = 90,
    [int]$PollIntervalSeconds = 2,
    [switch]$BuildFirst,
    [switch]$SkipThinkSmoke
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Wait-Http200 {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds,
        [Parameter(Mandatory = $true)][int]$PollSeconds
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -SkipCertificateCheck
            if ($resp.StatusCode -eq 200) {
                return $true
            }
        }
        catch {
        }
        Start-Sleep -Seconds $PollSeconds
    }

    return $false
}

function Wait-ServiceHealthy {
    param(
        [Parameter(Mandatory = $true)][string]$ServiceName,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds,
        [Parameter(Mandatory = $true)][int]$PollSeconds
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $containerId = (& docker compose -f $ComposeFile ps -q $ServiceName | Select-Object -First 1).Trim()
        if ($containerId -and $containerId.StartsWith("Usage:")) {
            Start-Sleep -Seconds $PollSeconds
            continue
        }
        if (-not $containerId) {
            Start-Sleep -Seconds $PollSeconds
            continue
        }

        $health = (& docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" $containerId).Trim()
        if ($health -eq "healthy") {
            return $true
        }

        Start-Sleep -Seconds $PollSeconds
    }

    return $false
}

function Invoke-ThinkSmoke {
    param([string]$Url)

    $body = @{ prompt = "rolling update smoke check"; task_type = "reasoning" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri $Url -Method Post -ContentType "application/json" -Body $body -TimeoutSec 90 -SkipCertificateCheck

    if ($null -eq $response -or -not $response.PSObject.Properties.Name.Contains("status")) {
        throw "Think smoke response is invalid."
    }

    return $response
}

if (-not (Test-Path $ComposeFile)) {
    throw "docker-compose.yml nuk u gjet: $ComposeFile"
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEUROSONIC ROLLING UPDATE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compose: $ComposeFile"
Write-Host "Root:    $ProjectRoot"
Write-Host ""

Push-Location $ProjectRoot
try {
    if ($BuildFirst) {
        Write-Host "[0/3] Building backend image..." -ForegroundColor Yellow
        & docker compose -f $ComposeFile build backend | Out-Host
    }

    Write-Host "[1/3] Ensuring service topology is up..." -ForegroundColor Yellow
    & docker compose -f $ComposeFile up -d --no-deps backend web | Out-Host

    if (-not (Wait-Http200 -Url $HealthUrl -TimeoutSeconds $HealthTimeoutSeconds -PollSeconds $PollIntervalSeconds)) {
        throw "API health nuk u be 200 ne kohe: $HealthUrl"
    }
    Write-Host "  ✅ Initial health OK" -ForegroundColor Green

    $services = @("backend")
    $step = 2
    foreach ($service in $services) {
        Write-Host "[$step/3] Recreating $service ..." -ForegroundColor Yellow
        & docker compose -f $ComposeFile up -d --force-recreate --no-deps $service | Out-Host

        if (-not (Wait-ServiceHealthy -ServiceName $service -TimeoutSeconds $HealthTimeoutSeconds -PollSeconds $PollIntervalSeconds)) {
            throw "Service $service nuk arriti gjendjen healthy."
        }

        if (-not (Wait-Http200 -Url $HealthUrl -TimeoutSeconds $HealthTimeoutSeconds -PollSeconds $PollIntervalSeconds)) {
            throw "API health dështoi pas recreate të $service"
        }

        if (-not $SkipThinkSmoke) {
            $thinkResult = Invoke-ThinkSmoke -Url $ThinkUrl
            Write-Host "  ✅ Think smoke OK on $service (status=$($thinkResult.status), engine=$($thinkResult.engine))" -ForegroundColor Green
        }
        else {
            Write-Host "  ✅ Health OK on $service (smoke skipped)" -ForegroundColor Green
        }

        $step++
    }

    Write-Host "[3/3] Final service status:" -ForegroundColor Yellow
    & docker compose -f $ComposeFile ps | Out-Host

    Write-Host ""
    Write-Host "✅ Rolling update completed successfully." -ForegroundColor Green
}
finally {
    Pop-Location
}
