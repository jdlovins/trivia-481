web: daphne -b 0.0.0.0 -p $PORT triviagame.asgi:channel_layer -v2
worker: python manage.py runworker -v2
release: python manage.py migrate