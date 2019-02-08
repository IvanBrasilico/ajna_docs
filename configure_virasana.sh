#!/bin/sh
# Precisa ser executado com sudo
set -x 

# Copiar diretorio static para Servidor WEB
sudo mkdir /var/www/html/static
sudo cp -r virasana/virasana/static/* /var/www/html/static

# Configurar Nginx
# Colocar linhas abaixo em /etc/nginx/sites-available/default
#
# server {
#	listen 80 default_server;
#    (...)
#	location /virasana {
#		proxy_pass http://127.0.0.1:5001;
#	}


sed -i 's,/home/ivan,'"$HOME"',g' virasana/supervisor_*
cp virasana/supervisor*.conf /etc/supervisor/conf.d/
mkdir /var/log/virasana
supervisorctl reread
supervisorctl reload