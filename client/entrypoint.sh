#!/bin/bash

#Tempo para garantir que o banco de dados suba antes do Django
echo "Esperando banco"
sleep 15

python manage.py collectstatic --noinput

echo "Migrations"
python manage.py makemigrations
python manage.py migrate --run-syncdb

echo "Iniciando Django"
python manage.py runserver 0.0.0.0:8000