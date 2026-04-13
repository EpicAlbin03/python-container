#!/bin/sh

# Exit immediately if any command fails
set -e

# Load env variables
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

echo 'Running migrations...'
uv run python manage.py makemigrations
uv run python manage.py migrate

if [[ -v DJANGO_SUPERUSER_USERNAME && -v DJANGO_SUPERUSER_EMAIL && -v DJANGO_SUPERUSER_PASSWORD ]]; then
    echo 'Creating super user...'
    uv run python manage.py createsuperuser --noinput || echo 'Super user already created'
fi

# echo 'Collecting static files...'
# uv run python manage.py collectstatic --noinput

# Execute the main command (passed as arguments)
exec "$@"