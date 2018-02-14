[![Build Status](https://travis-ci.org/IvanBrasilico/AJNA_MOD.svg?branch=master)](https://travis-ci.org/IvanBrasilico/AJNA_MOD) [![codecov](https://codecov.io/gh/IvanBrasilico/AJNA_MOD/branch/master/graph/badge.svg)](https://codecov.io/gh/IvanBrasilico/AJNA_MOD) [![Build status](https://ci.appveyor.com/api/projects/status/0avweqwyqgx4hdrn?svg=true)](https://ci.appveyor.com/project/IvanBrasilico/ajna-mod)


# AJNA

Visão computacional e aprendizado de máquina aplicados à vigilância e repressão aduaneira


Módulos:

## ajna_commons
Biblioteca com funções e classes utilizadas em várias aplicações do AJNA

### Instalação 
Este módulo está marcado como requerido em TODAS as aplicações, portanto, no deploy, será automaticamente instalado pelo pip (requirements.txt) e/ou pelo setuptools(setup.py). 

### Instalação desenvolvedor
Recomenda-se, caso queira-se um ambiente para desenvolvimento e edição, e geração de documentação clonar todos os repositórios conforme instruções dentro da pasta ajna_doc. Depois, dentro dos demais módulos, digitar as seguintes linhas:
```
$ pip uninstall ajna_commons
$ ln -s ../ajna_commons/ajna_commons .
```
## ajna_cov

Interface(s) para cadastramento de fontes de imagens, configuração de parâmetros, primeiros tratamentos, etc. Faz também a aquisição de imagens, vídeos e outros dados. Para ser instalado na(s) rede(s) em que ficam as imagens a serem adquiridas.

## bhadrasana - sentinela

Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco. Disponibiliza seus dados em Restful API.

Aquisição de dados. Serviço com scripts que acessam sistemas fechados e dados públicos, estruturados e não estruturados, guardando em coleções/Bancos de Dados. Disponibiliza seus dados em Restful API.

Constituído de uma aplicação web e wevbservice, e diversos workers controlados pelo Celery

## virasana - heroi

Interface para visualização e busca de imagens, recebimento de alertas e execução, manual ou automática, dos algoritmos do módulo ml_code nas imagens. Disponibiliza seus dados em Restful API.

Aquisição de imagens. Serviço com Scripts que acessam as fontes de imagens cadastradas, validam, pré-processam, fazem reconhecimento de caracteres, validam, monitoram mudanças, etc e copiam para um diretório único. Disponibiliza seus dados em Restful API.

Constituído de uma aplicação web e wevbservice, e diversos workers controlados pelo Celery

## padma - busca da verdade

Coleção de algoritmos de machine learning plugáveis e servidos em WebService. Basicamente é uma API que recebe dados e devolve predições.

Constituído de uma aplicação web e wevbservice, e diversos workers controlados pelo Celery

## notebooks

Rascunhos. Aproveitar a interatividade e praticidade do Jupyter Notebook para fazer e documentar as análises exploratórias de dados, treinamento e teste de algoritmos de aprendizado e projetar/validar scripts de data_aq


### Instalação 
Para instalar os módulos bhadrasana, padma, virasana:

```
$git clone <nome do repositório>
$cd <nome do módulo>
$python3 -m venv <modulo>-venv
$. <modulo>-venv/bin/activate
$python setup.py install
```
Ex:

```
$git clone https://github.com/IvanBrasilico/virasana.git
$cd virasana
$python3 -m venv virasana-venv
$. virasana-venv/bin/activate
(virasana-venv)$python setup.py install
(virasana-venv)$python -m pytest (roda os testes automatizados)
(virasana-venv)$./virasana/celery.sh (inicia os workers do serviço celery)
(virasana-venv)$ python virasana/app.py (inicia o servidor web/api)
```

### Instalação desenvolvedor

Clonar o módulo raiz ajna_doc

```
$git clone https://github.com/IvanBrasilico/ajna_docs.git
$cd ajna_docs
$python3 -m venv ajna-venv
$. ajna-venv/bin/activate
(ajna-venv)$python setup.py develop
$deactivate
```

Repetir os passos acima para os demais módulos, DENTRO do diretório ajna_docs

A estrutura de diretórios ficará assim:

* ajna_docs
 * ajna_commons
 * bhadrasana
 * notebooks
 * padma
 * virasana


Para poder editar o ajna_commons num local único (pois será instalada uma cópia em cada venv criado), dentro de cada diretório/módulo, com o venv ativo, digite:

```
$ pip uninstall ajna_commons
$ ln -s ../ajna_commons/ajna_commons .
```

