#!/bin/sh
set -e

# Wait for MySQL to be ready
until python /app/hms/wait_for_db.py; do
  echo "Waiting for database to be ready..."
  sleep 1
done

# Run migrations
python /app/manage.py migrate

# Collect static files
python /app/manage.py collectstatic --noinput

# Start Gunicorn
gunicorn hms.wsgi:application --bind 0.0.0.0:8000