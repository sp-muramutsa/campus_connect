#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Use environment variables for credentials
python manage.py createsuperuser --noinput --username $SUPERUSER_NAME --email $SUPERUSER_EMAIL || true

# Error happens here:
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$SUPERUSER_NAME').first().set_password('$SUPERUSER_PASSWORD'); User.objects.filter(username='$SUPERUSER_NAME').first().save()" | python manage.py shell