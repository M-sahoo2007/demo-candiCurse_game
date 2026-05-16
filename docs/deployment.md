# Deployment Guide

## Docker

1. Build and start containers:
```bash
docker-compose up --build
```
2. The web app runs at `http://localhost:8000`.

## PostgreSQL Ready

Set `DATABASE_URL=postgres://user:password@db:5432/candyverse` in `.env` when using Docker/PostgreSQL.

## Render / Railway

- Configure environment variables from `.env`
- Use `Dockerfile` as the deployment image
- Ensure `gunicorn` is installed and `Procfile` points to the `web` process

## Collect static files

In production:
```bash
python manage.py collectstatic --noinput
```

## Additional production recommendations

- Set `DEBUG=False`
- Set `SECRET_KEY` to a strong unique value
- Configure `ALLOWED_HOSTS`
- Use HTTPS and secure cookie settings
- Use a managed Postgres service for production database reliability
