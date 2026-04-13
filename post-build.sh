#!/bin/sh

# Exit immediately if any command fails
set -e

# echo 'Run migrations'
uv run python manage.py makemigrations
uv run python manage.py migrate

# echo 'Create Super User'
uv run python manage.py createsuperuser --noinput || echo "Super user already created"

# echo 'Collect Static'
# uv run python manage.py collectstatic --noinput