#!/bin/sh
python3 manage.py makemigrations Recycler
python3 manage.py migrate
python3 manage.py createsuperuser
exec "$@"