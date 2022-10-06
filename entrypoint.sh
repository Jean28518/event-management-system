#!/bin/sh
python manage.py migrate --no-input
python manage.py compilemessages
python manage.py collectstatic --no-input

gunicorn event_management_system.wsgi:application --bind 0.0.0.0:8000