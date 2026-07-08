# Docker Compose: Local development

This repo includes `docker-compose.yml` to run the Django web app, Redis, Celery worker and Celery beat for local integration testing.

Quick start:

```bash
# copy env example
cp .env.example .env
# build and start services
docker compose up --build
```

Services:
- `web` — Django + Gunicorn on port 8000
- `redis` — Redis broker for Celery
- `worker` — Celery worker for background tasks
- `beat` — Celery beat for periodic tasks

Run migrations before using the site (in a separate terminal):

```bash
# open a shell in the web container
docker compose run --rm web python manage.py migrate --noinput
# create superuser if needed
docker compose run --rm web python manage.py createsuperuser
```

Stopping:

```bash
docker compose down
```

Notes:
- Ensure your `.env` has a secure `SECRET_KEY` in production.
- The `Dockerfile` exposes port `8000` and runs `gunicorn` by default.
- For development, you can run the Django dev server instead of Gunicorn by overriding the `command` in the `web` service.
