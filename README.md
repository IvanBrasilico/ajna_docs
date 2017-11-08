[![Build Status](https://travis-ci.org/IvanBrasilico/raspa-preco.svg?branch=master)](https://travis-ci.org/IvanBrasilico/raspa-preco) [![codecov](https://codecov.io/gh/IvanBrasilico/raspa-preco/branch/master/graph/badge.svg)](https://codecov.io/gh/IvanBrasilico/raspa-preco)

# AJNA

Visão computacional e aprendizado de máquina 


Módulos:

## admin_interface

Interface para cadastramento de fontes de imagens, usuários, configuração de parâmetros, etc

## image_aq

Aquisição de imagens. Serviço com Scripts que acessam as fontes de imagens cadastradas, validam, pré-processam, fazem reconhecimento de caracteres, validam, monitoram mudanças, etc e copiam para um diretório único. Disponibiliza seus dados em Restful API.

## data_aq 

Aquisição de dados. Serviço com scripts que acessam sistemas fechados e dados públicos, estruturados e não estruturados, guardando em coleções/Bancos de Dados. Disponibiliza seus dados em Restful API.

## sentinela
 
Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco. Disponibiliza seus dados em Restful API.

## chakra

Interface para visualização e busca de imagens, recebimento de alertas e execução, manual ou automática, dos algoritmos do módulo ml_code nas imagens. Disponibiliza seus dados em Restful API.

## ml_code

Coleção de algoritmos de machine learning plugáveis e servidos em WebService
