#!/bin/sh

# Очікування запуску бази даних
echo "Waiting for postgres..."
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Виконання міграцій
python manage.py migrate

# Запуск flake8 для перевірки коду
flake8 .

# Запуск сервера
python manage.py runserver 0.0.0.0:8000
