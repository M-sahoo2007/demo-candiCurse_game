param(
  [string] $Owner,
  [string] $Repo,
  [string] $Branch = 'main'
)

if (-not $Owner -or -not $Repo) {
  Write-Host "Usage: .\scripts\protect-branch.ps1 -Owner <owner> -Repo <repo> [-Branch <branch>]" -ForegroundColor Yellow
  exit 2
}

Write-Host "Protecting branch $Branch on $Owner/$Repo"

$body = @{
  required_status_checks = @{ strict = $true; contexts = @('django.yml') }
  enforce_admins = $true
  required_pull_request_reviews = @{ dismiss_stale_reviews = $false }
} | ConvertTo-Json -Depth 5

gh api --method PUT "/repos/$Owner/$Repo/branches/$Branch/protection" -f "$body"

Write-Host "Branch protection applied."
