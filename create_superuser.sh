#!/bin/sh

set -e

echo "Применение миграций..."
python manage.py makemigrations
python manage.py migrate

if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists()"; then
    echo "Суперпользователь уже существует."
else
    echo "Создание суперпользователя..."
    python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"

    echo "Установка пароля для суперпользователя..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User  = get_user_model();
user = User.objects.get(username='$DJANGO_SUPERUSER_USERNAME');
user.set_password('$DJANGO_SUPERUSER_PASSWORD');
user.save();
"
fi

echo "Запуск сервера..."
python manage.py runserver 0.0.0.0:8002
