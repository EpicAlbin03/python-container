#!/bin/bash

# Exit immediately if any command fails
set -e

# Run Django migrations
echo 'Running migrations...'
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create super user if env variables exists (only in dev)
if [[ -v $DJANGO_SUPERUSER_USERNAME && -v $DJANGO_SUPERUSER_EMAIL && -v $DJANGO_SUPERUSER_PASSWORD ]]; then
    echo 'Creating super user...'
    uv run python manage.py createsuperuser --noinput || echo 'Super user already created'
fi

# Collect static files in prod
# if [ "$DJANGO_DEBUG" == "False" ]; then
#     echo 'Collecting static files...'
#     uv run python manage.py collectstatic --noinput
# fi

# Execute the main command (passed as arguments)
exec "$@"