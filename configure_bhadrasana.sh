#!/bin/sh
# Precisa ser executado com sudo
set -x


# Configurar Nginx
echo "Colocar linhas abaixo em /etc/nginx/sites-available/default abaixo de listen 80 default server"
#
# server {
#	listen 80 default_server;
#    (...)
echo "location /bhadrasana {"
echo "		proxy_pass http://127.0.0.1:5000; }"

sed -i 's,/home/ivan,'"$HOME"',g' bhadrasana/supervisor_*
cp bhadrasana/supervisor*.conf /etc/supervisor/conf.d/
mkdir /var/log/bhadrasana
supervisorctl reread
supervisorctl reload
