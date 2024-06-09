#!/bin/sh

echo "Apply database migrations"
python app/manage.py makemigrations
python app/manage.py migrate


if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    echo "Create Super User"
    python app/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python app/manage.py runserver 0.0.0.0:8000