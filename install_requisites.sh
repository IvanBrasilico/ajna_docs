#!/bin/bash
set -x

# No CentOS mudar apt para yum

# Instalar Servidor REDIS
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Instalar Servidor MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt update
sudo apt install mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

#Nginx (Opcional Apache)
# sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
sudo ufw enable

#Supervisor - para iniciar servicos
sudo apt install supervisor
sudo systemctl enable supervisor

# Configurar AJNA_DIR e AJNA_LOG_DIR no supervisor
# Pode ser necessário adaptar para o ambiente de instalação
sudo echo "environment=AJNA_HOME=/home/ivan/ajna,AJNA_LOG_DIR=/var/log/ajna" >> /etc/supervisor/supervisord.conf
sudo systemctl start supervisor
sudo mkdir /var/log/ajna


# Python 3 configuracao
sudo apt install python3-pip
sudo apt install python3-venv
sudo pip3 install --upgrade wheel setuptools venv pip
