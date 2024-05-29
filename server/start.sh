#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn server.wsgi:application -w 1 -k gthread -b 0.0.0.0:80
