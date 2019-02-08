#!/bin/bash
set -x

# Instalacao do ajna_core e da documentacao
cd $HOME
# git clone https://github.com/IvanBrasilico/ajna.git
cd ajna
pip install --upgrade --user pip wheel setuptools
ln -s commons/ajna_commons .
python3 -m venv ajna-venv
. ajna-venv/bin/activate
pip install .

# Para adicionar usuarios na base:
python ajna_commons/scripts/adduser.py

# Copiar docs para diretorio do nginx para acessando localhost/help abrir a documentacao do AJNA
# Pode ser necessario configurar o Servidor web especifico (Nginx ou Apache)
sudo cp -r _build/html /var/www/html/ajna


