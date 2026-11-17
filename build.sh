#!/usr/bin/env bash
# Render build step. Exit on the first error so a broken build never goes live.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py bootstrap_site

if [ "${SEED_DEMO:-false}" = "true" ]; then
  python manage.py seed_demo
fi
