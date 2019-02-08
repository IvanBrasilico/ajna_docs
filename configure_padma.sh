#!/bin/sh
# Precisa ser executado com sudo
set -x

# Configurar Nginx
echo "Colocar linhas abaixo em /etc/nginx/sites-available/default abaixo de listen 80 default server"
#
# server {
#	listen 80 default_server;
#    (...)
echo "location /padma {"
echo "		proxy_pass http://127.0.0.1:5002; }"

sed -i 's,/home/ivan,'"$HOME"',g' padma/supervisor_*
cp padma/supervisor*.conf /etc/supervisor/conf.d/
mkdir /var/log/padma
supervisorctl reread
supervisorctl reload

