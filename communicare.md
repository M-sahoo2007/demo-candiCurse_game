# Communicare

## Summary of work completed

This document captures all changes made during the current project work, including CI fixes, dependency auditing, Docker Compose support, local test verification, and branch protection guidance.

### 1. CI workflow updates

File: `.github/workflows/django.yml`

- Added a broader Python matrix: `3.10`, `3.11`, `3.12`, `3.13`, `3.14`.
- Quoted Python versions to avoid YAML float parsing problems (`3.10` should not become `3.1`).
- Enforced dependency auditing with `pip-audit` so the workflow fails when vulnerabilities are detected.
- Kept `actions/checkout@v4` and `actions/setup-python@v5` for compatibility with current runners.

### 2. Docker Compose integration

File: `docker-compose.yml`

- Added `web` service:
  - Builds the existing `Dockerfile`.
  - Runs `gunicorn candyverse.wsgi:application --bind 0.0.0.0:8000`.
  - Mounts the project and exposes port `8000`.
  - Uses `.env` for configuration.
- Added `redis` service:
  - Uses `redis:7`.
  - Exposes `6379`.
- Added `worker` service:
  - Runs a Celery worker for background tasks.
  - Depends on `redis`.
- Added `beat` service:
  - Runs Celery beat for scheduled tasks.
  - Depends on `redis`.

File: `.env.example`

- Added Redis/Celery environment variables:
  - `CELERY_BROKER_URL`
  - `CELERY_RESULT_BACKEND`
  - `REDIS_URL`

### 3. Local docs

File: `docs/DOCKER_COMPOSE.md`

- Added Docker Compose usage instructions.
- Included migration and superuser creation commands.
- Explained how to stop services and noted production considerations.

### 4. Branch protection automation scripts

Files:
- `scripts/protect-branch.sh`
- `scripts/protect-branch.ps1`

These scripts use GitHub CLI (`gh`) to apply branch protection to `main` with:
- Required status checks: `django.yml`
- Strict status check enforcement
- Admin enforcement enabled
- Required pull request review settings

Usage examples:
```bash
./scripts/protect-branch.sh M-sahoo2007 demo-candiCurse_game main
```
```powershell
.\scripts\protect-branch.ps1 -Owner M-sahoo2007 -Repo demo-candiCurse_game -Branch main
```

### 5. Local verification

Commands run successfully in the local project environment:

```bash
python manage.py migrate --noinput
python manage.py test --verbosity=2
```

Test result:
- `1 test` passed
- No migration errors
- Local app schema is up to date

### 6. Remaining manual steps

Because Docker was not available in this execution environment, the following steps remain for local completion:

```bash
cp .env.example .env
docker compose up --build -d
docker compose run --rm web python manage.py migrate --noinput
docker compose run --rm web python manage.py createsuperuser
docker compose run --rm web python manage.py test
```

For protected branch enforcement, run one of the scripts above locally after authenticating with GitHub CLI.

### 7. Notes

- The CI workflow now makes dependency auditing strict and will block merges if `pip-audit` finds issues.
- `communicare.md` captures the entire conversation and work items in one place as requested.
