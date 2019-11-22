#!/bin/sh

# Start Gunicorn processes
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
echo Starting Gunicorn.
exec gunicorn main_interface.wsgi:application \
    --bind :8000 \
    --workers 3
