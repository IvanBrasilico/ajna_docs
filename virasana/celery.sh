cd ..
. venv-sentinela/bin/activate
celery -A virasana.app.virasana.celery worker --loglevel=info