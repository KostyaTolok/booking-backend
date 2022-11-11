#!/bin/sh

echo "Applying database migrations"
python manage.py migrate

python manage.py loaddata fixtures

python manage.py collectstatic --noinput

echo "Starting server on 0.0.0.0:3000"
gunicorn search.wsgi:application --bind 0.0.0.0:3000
