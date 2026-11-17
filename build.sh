#!/usr/bin/env bash
# Render build step. Runs during container image creation (no database access).
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
