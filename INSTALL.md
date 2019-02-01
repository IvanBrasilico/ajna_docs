* [Módulos](#Módulos)
  * [Geral](#Geral)
  * [Desenvolvimento](#Desenvolvimento)
  * [core](#Core)
  * [virasana](#virasana)
  * [bhadrasana](#bhadrasana)
  * [padma](#padma)

* [Estrutura] (#Estrutura)


# Módulos

## Geral

Os arquivos install_*.sh podem ser utilizados para instalação automática dos módulos ou como guia.

Os requisitos do Sistema são Python3.5+, Redis, MongoDB  

Para instalação em Servidor, é necessário instalar um Servidor WEB (Nginx ou Apache) e habilitar o mod_proxy para
os servidores AJNA. Para inicializar os serviços AJNA, é recomendado o uso do Supervisor. São fornecidos exemplos
e scripts para estas configurações nos arquivos configure_*.sh e supervisor_*.sh. 

## Desenvolvimento

Recomenda-se clonar primeiro o "core" ajna na pasta ´home/user/ajna´ e depois todos os repositórios
 dentro da pasta ajna.
 
Depois, dentro de cada pasta de cada módulo e com venv ativo, digitar:

```
(venv)$ ln -s ../commons/ajna_commons .
(venv)$ pip install -e .[dev]
```

## core
Core ou commons/docs. Contém as configurações para gerar documentação automática e as bibliotecas comnuns.
 
Este módulo. Requerido para todos os demais módulos AJNA.

Clonar o módulo raiz ajna e rodar install_*.sh no projeto ajna.

Automático:

```
$git clone https://github.com/IvanBrasilico/ajna.git
$cd ajna
$./install_requisites.sh
$./install_core.sh
```

Manual (presumindo que requisitos estão instalados e atualizados):

```
$git clone https://github.com/IvanBrasilico/ajna.git
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

## bhadrasana

Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco.

A instalação segue exatamente os mesmos passos do virasana:

Rodar install_bhadrasana.sh no diretório raiz do ajna.

Ir para diretório bhadrasana e rodar "./celery.sh" e "python wsgi_sentinela_debug.py" para testar instalação. 

Rodar configure_bhadrasana.sh para instalar as configurações do supervisor e do apache/nginx.

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
$git clone https://github.com/IvanBrasilico/virasana.git
$cd virasana
$python3 -m venv virasana-venv
$. virasana-venv/bin/activate
(virasana-venv)$pip install .
(virasana-venv)$python -m pytest (roda os testes automatizados)
(virasana-venv)$./virasana/celery.sh (inicia os workers do serviço celery)
(virasana-venv)$ python virasana/app.py (inicia o servidor web/api)
```

## Estrutura

A estrutura de diretórios ficará assim:

<pre>/ajna  
 ┬  
 ├  commons
 ├  bhadrasana
 ├  padma
 └  virasana
</pre>

Para poder editar o ajna_commons num local único (senão será necessário instalar uma cópia em cada venv criado), 
dentro de cada diretório/módulo, com o venv respectivo ativo, digite:

```
$ pip uninstall ajna_commons
$ ln -s ../ajna_commons/ajna_commons .
```
