#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py createsuperuser --noinput --username "$SUPERUSER_NAME" --email "$SUPERUSER_EMAIL" || true

(echo "$SUPERUSER_PASSWORD"; echo "$SUPERUSER_PASSWORD") | python manage.py changepassword "$SUPERUSER_NAME"
