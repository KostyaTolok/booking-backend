#!/bin/sh

echo "Applying database migrations"
python manage.py migrate

python manage.py loaddata cities
python manage.py loaddata hotels
python manage.py loaddata hotel_images
python manage.py loaddata rooms
python manage.py loaddata room_images

python manage.py collectstatic --noinput

echo "Starting server on 0.0.0.0:3000"
python manage.py runserver 0.0.0.0:3000
