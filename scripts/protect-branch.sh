#!/usr/bin/env bash
# Usage: ./scripts/protect-branch.sh OWNER REPO BRANCH
# Example: ./scripts/protect-branch.sh M-sahoo2007 demo-candiCurse_game main

set -euo pipefail

OWNER=${1:-}
REPO=${2:-}
BRANCH=${3:-main}

if [ -z "$OWNER" ] || [ -z "$REPO" ]; then
  echo "Usage: $0 OWNER REPO [BRANCH]"
  exit 2
fi

echo "Protecting branch $BRANCH on $OWNER/$REPO"

# Require status checks to pass (example: Django CI)
gh api --method PUT "/repos/$OWNER/$REPO/branches/$BRANCH/protection" \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts='["django.yml"]' \
  -F enforce_admins=true \
  -F required_pull_request_reviews.dismiss_stale_reviews=false

echo "Branch protection applied."
