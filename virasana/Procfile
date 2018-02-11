web: gunicorn wsgi:app
worker: celery -E -A virasana.app.celery worker --loglevel=info