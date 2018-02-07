cd ..
. venv-sentinela/bin/activate
celery -A virasana.virasanaapp.celery worker --loglevel=info