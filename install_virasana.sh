# Virasana - Servidor de imagens
git clone https://github.com/IvanBrasilico/virasana.git
cd virasana/
ln -s ../commons/ajna_commons .
python3 -m venv virasana-venv
. virasana-venv/bin/activate
pip install .

# python wsgi.py -- para testar
# ./configure_virasana.sh -- para configurar Supervisor e Nginx/Apache
