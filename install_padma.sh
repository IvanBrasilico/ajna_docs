#!/bin/bash
set -x

# PADMA - Servidor de imagens
git clone https://github.com/IvanBrasilico/padma.git
cd padma/
ln -s ../commons/ajna_commons .
python3 -m venv padma-venv
. padma-venv/bin/activate
pip install .

# Abaixo é feita a clonagem do TensorFlow Object Detection
git clone https://github.com/IvanBrasilico/models.git

# python wsgi_debug.py -- para testar Servidor API
# python server.py -- para testar Servidor de modelos
# ./configure_padma.sh -- para configurar Supervisor e Nginx/Apache
# Pode ser necessário baixar à parte os modelos salvos e colocá-los nos diretórios corretos
# Diretórios de modelos em padma/padma/models (Não confundir com models do TensorFlow, um diretorio acima)