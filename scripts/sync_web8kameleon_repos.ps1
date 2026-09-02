param(
    [string]$Org = "Web8kameleon-hub",
    [string]$WebsiteRepo = "www.neurosonic.eu",
    [string]$OutputMarkdown = "docs/community/WEB8KAMELEON_REPOS.md",
    [string]$OutputJson = "docs/community/web8kameleon_repos.json",
    [string]$Token = $env:GITHUB_TOKEN
)

$ErrorActionPreference = "Stop"

function Get-Repositories {
    param(
        [string]$Organization,
        [string]$AuthToken
    )

    $headers = @{
        "Accept"     = "application/vnd.github+json"
        "User-Agent" = "neurosonic-repo-sync"
    }

    if ($AuthToken) {
        $headers["Authorization"] = "Bearer $AuthToken"
    }

    function Get-Paged {
        param([string]$BaseUrl)

        $allItems = @()
        $pageNumber = 1
        $perPageCount = 100

        while ($true) {
            $url = "${BaseUrl}?per_page=$perPageCount&page=$pageNumber&type=public&sort=updated"
            $batch = Invoke-RestMethod -Uri $url -Headers $headers -Method Get

            if (-not $batch -or $batch.Count -eq 0) {
                break
            }

            $allItems += $batch

            if ($batch.Count -lt $perPageCount) {
                break
            }

            $pageNumber += 1
        }

        return $allItems
    }

    try {
        return Get-Paged -BaseUrl "https://api.github.com/orgs/$Organization/repos"
    }
    catch {
        if ($_.Exception.Message -match '404') {
            Write-Host "Org '$Organization' not found or inaccessible; falling back to user repositories."
            return Get-Paged -BaseUrl "https://api.github.com/users/$Organization/repos"
        }
        throw
    }
}

function Ensure-ParentDirectory {
    param([string]$Path)

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$markdownPath = Join-Path $root $OutputMarkdown
$jsonPath = Join-Path $root $OutputJson

Ensure-ParentDirectory -Path $markdownPath
Ensure-ParentDirectory -Path $jsonPath

Write-Host "Fetching repositories for organization '$Org'..."
$repos = Get-Repositories -Organization $Org -AuthToken $Token

if (-not $repos -or $repos.Count -eq 0) {
    throw "No repositories found for '$Org'. If the org is private, set GITHUB_TOKEN."
}

$mapped = $repos |
Sort-Object -Property name |
ForEach-Object {
    [PSCustomObject]@{
        name                 = $_.name
        full_name            = $_.full_name
        html_url             = $_.html_url
        description          = $_.description
        homepage             = $_.homepage
        default_branch       = $_.default_branch
        pushed_at            = $_.pushed_at
        archived             = $_.archived
        visibility           = $_.visibility
        is_primary_site_repo = ($_.name -eq $WebsiteRepo)
    }
}

$mapped | ConvertTo-Json -Depth 4 | Set-Content -Path $jsonPath -Encoding UTF8

$generatedUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss 'UTC'")
$lines = @(
    "# Web8kameleon Hub Repositories",
    "",
    "Generated: $generatedUtc",
    "",
    "Primary site repository: [$WebsiteRepo](https://github.com/$Org/$WebsiteRepo)",
    "",
    "| Repository | Description | Homepage | Last Push |",
    "|---|---|---|---|"
)

foreach ($repo in $mapped) {
    $description = if ($repo.description) { $repo.description } else { "-" }
    $homepage = if ($repo.homepage) { "[link]($($repo.homepage))" } else { "-" }
    $lastPush = if ($repo.pushed_at) { [DateTime]::Parse($repo.pushed_at).ToString("yyyy-MM-dd") } else { "-" }
    $repoLink = "[$($repo.name)]($($repo.html_url))"
    $lines += "| $repoLink | $description | $homepage | $lastPush |"
}

$lines -join "`r`n" | Set-Content -Path $markdownPath -Encoding UTF8

Write-Host "Generated: $OutputMarkdown"
Write-Host "Generated: $OutputJson"
Write-Host "Done."
