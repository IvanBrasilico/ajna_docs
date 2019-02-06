#!/bin/sh
set -x 

# Configurar Nginx
echo "Colocar linhas abaixo em /etc/nginx/sites-available/default abaixo de listen 80 default server"
#
# server {
#	listen 80 default_server;
#    (...)
echo "location /padma {"
echo "		proxy_pass http://127.0.0.1:5002; }"


cp padma/supervisor*.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/padma
sudo supervisorctl reread
