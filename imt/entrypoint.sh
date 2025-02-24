#!/bin/bash
echo "Running migrate..."
python manage.py migrate

echo "Running collectstatic..."
python manage.py collectstatic  --noinput

echo "Starting server....$DJANGO_ENV"

# Start the application using Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 2 imt_mng.wsgi:application
