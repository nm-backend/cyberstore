#!/usr/bin/env bash
# Render runtime start step. Runs inside the active container with full PostgreSQL access.
set -o errexit

python manage.py migrate --no-input
python manage.py bootstrap_site

if [ "${SEED_DEMO:-false}" = "true" ]; then
  python manage.py seed_demo
fi

exec gunicorn config.wsgi:application --workers 2 --timeout 60
