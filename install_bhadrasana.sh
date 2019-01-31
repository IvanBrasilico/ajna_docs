# Virasana - Servidor de imagens
git clone https://github.com/IvanBrasilico/bhadrasana.git
cd bhadrasana/
ln -s ../commons/ajna_commons .
python3 -m venv bhadrasana-venv
. bhadrasana-venv/bin/activate
pip install .

# python wsgi.py -- para testar
# ./celery.sh  -- para testar
# ./configure_bhadrasana.sh -- para configurar Supervisor e Nginx/Apache
