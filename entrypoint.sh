#!/bin/bash

# Run migrations
python manage.py migrate --no-input

# Create superuser (will only run once)
python manage.py create_default_superuser

mkdir -p /app/staticfiles
chown -R appuser:appuser /app/staticfiles

# Collect static files
python manage.py collectstatic --no-input

# Start the Gunicorn server debe ser el nombre de la carpeta donde está tu archivo wsgi.py.
# ¡CAMBIO AQUÍ! Ahora enlaza con 0.0.0.0:8080
gunicorn GestDocSi2.wsgi:application --bind 0.0.0.0:8080