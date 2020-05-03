#!/bin/sh
python3 manage.py makemigrations Recycler
python3 manage.py migrate
exec "$@"