* [Módulos](#Módulos)
  * [Geral](#Geral)
  * [Desenvolvimento](#Desenvolvimento)
  * [Produção](#Produção)
  * [core](#Core)
  * [virasana](#virasana)
  * [bhadrasana2](#bhadrasana2)
  * [padma](#padma)

* [Estrutura] (#Estrutura)


# Módulos

## Geral

Os arquivos install_*.sh podem ser utilizados para instalação automática
dos módulos ou como guia (necessário atualizar).

Os requisitos do Sistema são Python3.9+, MongoDB, MySQL  

Para instalação em Servidor, é necessário instalar um Servidor Apache e habilitar 
o mod_proxy e mod_ssl para os servidores AJNA. Para inicializar os serviços AJNA, 
é recomendado o uso do Supervisor. São fornecidos exemplos e scripts para estas 
configurações nos arquivos configure_*.sh e supervisor_*.sh. 

## Desenvolvimento

Recomenda-se clonar primeiro o "core" ajna_docs na pasta ´home/user/ajna´ e depois todos os repositórios
(virasana, bhadrasana2, ajna_api, ajna_bot) dentro da pasta ajna.

As pastas ficarão assim

* ajna
  * ajna_docs
  * virasana
  * bhadrasana2

Exemplo: 
Dentro de cada pasta de cada módulo e *com venv ativo*, após instalação, rodar os testes
e tentar rodar a app. Podem ter arquivos de configuração e variáveis de ambiente a serem 
adicionadas (que por motivos de segurança não estão no git e na documentação)
```
$ mkdir ajna
$ cd ajna
$ git clone https://github.com/IvanBrasilico/ajna_docs/
$ git clone https://github.com/IvanBrasilico/virasana/
$ cd virasana
$ python3 -m venv virasana-venv
$ . virasana-venv/bin/activate
(virasana-venv)$ pip install -e .[dev]
(virasana-venv)$ ln -s ../ajna_docs/commons/ajna_commons ajna_commons
(virasana-venv)$ ln -s ../bhadrasana2/bhadrasana bhadrasana
(virasana-venv)$ python -m pytest --cov=virasana  virasana/tests
(virasana-venv)$ tox
```

### Variáveis de ambiente
É necessário setar as variáveis de ambiente para configuração, senhas de Banco de Dados, etc.

```
export SQL_URI=mysql+pymysql://usuario:senha@servidor:3306/dbmercante
export SQL_USER=True
export MONGODB_URI=mongodb://usuario:senha@servidor:1352/ajna
export EMBARCACOES_SECRET_KEY="umasenha_aleatoria_gerada_por_uma_ferramenta"
```

No Servidor, estas variáveis podem ser setadas no prompt para testes, para produção colocá-las
na configuração do supervisor.

No desenvolvimento, é possível usar recursos da IDE ou bibliotecas como o python-dotenv.

## Produção

### Instalar e configurar apache
```
sudo dnf install httpd mod_proxy mod_ssl
sudo systemctl enable httpd
sudo systemctl start httpd
curl localhost
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
cat /etc/httpd/conf/httpd.conf
sudo nano /etc/httpd/conf.d/sites.conf (Adicionar caminho para o Servidor python/gunicorn)
EX:
<VirtualHost *:80>

ProxyPreserveHost On
ProxyPass /virasana/ http://127.0.0.1:5001/virasana/
ProxyPassReverse /virasana/ http://127.0.0.1:5001/virasana/

</VirtualHost> (Ctrl+X Salvar)

sudo httpd -t
sudo systemctl httpd reload
sudo systemctl restart httpd.service
````
(Ver no arquivo configuração_apache.md a **configuração do ssl**)

### Instalação dos módulos

Seguir os passos acima em desenvolvimento. Para testar, rodar o comando:
´´´
(virasana-venv)$ gunicorn wsgi_production:application -b localhost:5001
´´´

O comando acima deixa o gunicorn com a aplicação Flask virasana rodando na porta 5001. 
Ao acessar o endereço do Servidor apache (Ex: http://ajna1.rfoc.srf/virasana) o Apache
redirecionará as requisições para esta porta. A aplicação estará funcionando, mas sem 
a apresentação css e javascript. Copiar o index.html e a pasta static do Ajna para /var/www/html
(home do Apache). Será necessário certificar que o usuário do Apache tem permissão nas pastas.

### Instalação do supervisor

````
sudo dnf install supervisor.noarch
sudo touch /etc/supervisord.conf
sudo echo_supervisord_conf > /etc/supervisord.conf
sudo nano /etc/supervisord.conf
#incluir as linhas "[supervisord]
#environment=" com as variáveis de ambiente e 
#"[include]
#files = /etc/supervisord.d/*conf"
sudo systemctl enable supervisord
sudo systemctl start supervisord
#copiar do módulo do ajna o arquivo do supervisor para /etc/supervisord.d/ fazendo as adaptações necessárias
sudo supervisorctl reload  # É possível configurar supervisor para não precisar de sudo no seu usuário
sudo supervisorctl restart
sudo supervisorctl status  
````

### MariaDB

````
sudo dnf install mariadb-server
sudo systemctl start mariadb
sudo mysql_secure_installation  # Siga as instruções
mysql -u root -p
# Criar o banco de dados e usuário
# CREATE DATABASE db_mercante;
# CREATE USER 'adm'@'%' IDENTIFIED BY 'your_secure_password';
# GRANT ALL PRIVILEGES ON db_mercante.* TO 'adm'@'%';
# FLUSH PRIVILEGES;
#
sudo firewall-cmd --permanent --add-service=mysql
sudo firewall-cmd --reload
````

### SELinux

Em máquinas com SELinux é necessário rodar também os comandos abaixo:

```
$ sudo /usr/sbin/setsebool -P httpd_can_network_connect 1
$ sudo chcon -R -v -t httpd_sys_rw_content_t /var/www/html/index.html
$ sudo chcon -R -v -t httpd_sys_rw_content_t /var/www/html/static
$ sudo setsebool -P mysql_connect_any on
```

## core
Core ou commons/docs. Contém as configurações para gerar documentação automática e as bibliotecas comnuns.
 
Este módulo. Requerido para todos os demais módulos AJNA.

Clonar o módulo raiz ajna e rodar install_*.sh no projeto ajna.

Automático:

```
$git clone https://github.com/IvanBrasilico/ajna_docs
$cd ajna_docs
$./install_requisites.sh
$./install_core.sh
```

Manual (presumindo que requisitos estão instalados e atualizados):

```
$git clone https://github.com/IvanBrasilico/ajna_docs
$cd ajna
$python3 -m venv ajna-venv
$. ajna-venv/bin/activate
(ajna-venv)$pip install -e .[dev]
```


## virasana

Interface para visualização e busca de imagens.

Rodar install_virasana.sh no diretório raiz do ajna.

Ir para diretório virasana e rodar "./celery.sh" e "python wsgi_debug.py" para testar instalação. 

Rodar configure_virasana.sh para instalar as configurações do supervisor e do apache/nginx. Pode ser necessário
 editar os arquivos virasana/supervisor_* e revisar as configurações do apache/nginx manualmente para adaptar 
 ao ambiente utilizado. 

## bhadrasana2

Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco.

Contém também a aplicação Fichas

## padma

Coleção de algoritmos de machine learning plugáveis e servidos em WebService.

Rodar install_padma.sh no diretório raiz do ajna.

Ir para diretório padma e rodar "python modelserver.py" e "python wsgi_debug.py" para testar instalação. 

## Instalação manual 

Os arquivos install_* seguem a mesma sequência básica que pode ser realizada manualmente
 se desejado, para maior controle:
 
```
$git clone <nome do repositório>
$cd <nome do módulo>
$python3 -m venv <modulo>-venv
$. <modulo>-venv/bin/activate
$pip install .
```
Ex:

```
$cd /home/ajna/
$mkdir apps
$cd apps
$mkdir ajna
$cd ajna
$git clone https://github.com/IvanBrasilico/ajna_docs.git
$cd ajna_docs
$python3 -m venv commons-venv
$. commons-venv/bin/activate
(commons-venv)$pip install .
(commons-venv)$python -m pytest (roda os testes automatizados)
```


```
$cd ..
$git clone https://github.com/IvanBrasilico/virasana.git
$cd virasana
$ln -s ../ajna_docs/commons/ajna_commons ajna_commons
$python3 -m venv virasana-venv
$. virasana-venv/bin/activate
(virasana-venv)$pip install .
(virasana-venv)$python -m pytest (roda os testes automatizados)
(virasana-venv)$ python virasana/wsgi_debug.py (inicia o servidor web/api)
```

```
$git clone https://github.com/IvanBrasilico/bhadrasana.git
$cd bhadrasana
$ln -s ../ajna_docs/commons/ajna_commons ajna_commons
$python3 -m venv bhadrasana-venv
$. bhadrasana-venv/bin/activate
(bhadrasana-venv)$pip install .
(bhadrasana-venv)$export NLTK_DATA=/home/ajna/apps/ajna/bhadrasana2/bhadrasana-venv/nltk_data/
(bhadrasana-venv)$python
>>>>>>import nltk
>>>>>>nltk.download('stopwords')
(bhadrasana-venv)$python -m pytest (roda os testes automatizados)
(bhadrasana-venv)$python bhadrasana/wsgi_debug.py (inicia o servidor web/api)
```




## Estrutura

A estrutura de diretórios ficará assim:

<pre>/ajna  
 ┬  
 ├  commons
 ├  bhadrasana2
 ├  padma
 └  virasana
</pre>

Para poder editar o ajna_commons num local único (senão será necessário instalar uma cópia em cada venv criado), 
dentro de cada diretório/módulo, com o venv respectivo ativo, digite:

```
$ pip uninstall ajna_commons
$ ln -s ../ajna_docs/commons/ajna_commons ajna_commons
```
