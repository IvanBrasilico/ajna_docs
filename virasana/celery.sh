cd ..
. venv-sentinela/bin/activate
celery -A virasana.virasana.celery worker --loglevel=info