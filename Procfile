web: daphne -b 0.0.0.0 -p $PORT triviagame.asgi:channel_layer -v2
worker: python manage.py runworker -v2
celery: celery worker -A triviagame -l info
release: python manage.py migrate