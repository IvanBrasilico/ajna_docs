[![Build Status](https://travis-ci.org/IvanBrasilico/AJNA_MOD.svg?branch=master)](https://travis-ci.org/IvanBrasilico/AJNA_MOD) [![codecov](https://codecov.io/gh/IvanBrasilico/AJNA_MOD/branch/master/graph/badge.svg)](https://codecov.io/gh/IvanBrasilico/AJNA_MOD) [![Build status](https://ci.appveyor.com/api/projects/status/0avweqwyqgx4hdrn?svg=true)](https://ci.appveyor.com/project/IvanBrasilico/ajna-mod)


# AJNA

Visão computacional e aprendizado de máquina aplicados à vigilância e repressão aduaneira


Módulos:

## ajna_commons
Biblioteca com funções e classes utilizadas em várias aplicações do AJNA

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
