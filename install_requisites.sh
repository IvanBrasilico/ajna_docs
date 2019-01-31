# No CentOS mudar para yum install

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


# Python 3 configuracao


# Python
sudo apt install python3-pip
sudo apt install python3-venv

