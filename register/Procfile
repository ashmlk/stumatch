web: gunicorn register.wsgi:application --env DJANGO_SETTINGS_MODULE='register.settings.production' --log-file -
worker: celery -A register worker -E -l info
celery_beat: celery -A register beat --loglevel=info