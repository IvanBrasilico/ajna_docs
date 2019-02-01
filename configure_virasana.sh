# Copiar diretorio static para Servidor WEB
sudo mkdir /var/www/html/static
sudo cp -r virasana/static/* /var/www/html/static

# Configurar Nginx
# Colocar linhas abaixo em /etc/nginx/sites-available/default
#
# server {
#	listen 80 default_server;
#    (...)
#	location /virasana {
#		proxy_pass http://127.0.0.1:5001;
#	}


cp virasana/supervisor*.conf /etc/supervisor/conf.d/