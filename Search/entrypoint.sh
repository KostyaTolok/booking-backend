#!/bin/sh

echo "Applying database migrations"
python manage.py migrate

echo "Starting server on 0.0.0.0:3000"
python manage.py runserver 0.0.0.0:3000
