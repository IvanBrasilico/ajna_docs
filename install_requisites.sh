#!/bin/bash
# Precisa ser executado com sudo
set -x

# No CentOS mudar apt para yum

# Instalar Servidor REDIS
apt install redis-server
systemctl start redis
systemctl enable redis

# Instalar Servidor MongoDB
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
apt update
apt install mongodb-org
systemctl start mongod
systemctl enable mongod

#Nginx (Opcional Apache)
apt install nginx
ufw allow 'Nginx HTTP'
ufw enable

#Supervisor - para iniciar servicos
apt install supervisor
systemctl enable supervisor
mkdir /var/log/ajna
systemctl start supervisor


# Python 3 configuracao
apt install python3-pip
apt install python3-venv
pip3 install --upgrade wheel setuptools venv pip
