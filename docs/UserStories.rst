.. contents:: Tópicos
 :depth: 2

`Voltar ao Indice <../index.html>`_


====================
Histórias de Usuário
====================

SENTINELA
=========

Módulo Parâmetros de Risco
==========================

Pré-processamento - Normalização
--------------------------------

Descrição:

Dada a multiplicidade de fontes de dados e formatos, como analista de risco,
preciso processar diversas planilhas e/ou arquivos csv.
Pode ser necessário fazer combinações entre essas planilhas,
mudar títulos, etc.
O caso de uso pode entregar o resultado no disco ou na memória.

São detalhamentos deste caso:

Mudar_Titulos_Planilha_CSV - OK

Planilhas de diversas fontes podem conter os mesmos dados com
títulos (nomes de campo) diferentes. É necessário

Combinar_Planilhas_CSV - OK

Para melhor filtragem, preciso configurar MERGE de planilhas que será
realizado repetidamente (sempre que novas bases forem carregadas)

Escolher Campos para exibição

TODO


Testes:
csv_handler_test.py
exemplos/test_cov.py
exemplos/test_carga.py

Observação:

Os dados de configuração poderão ser importados e exportados de/para arquivos CSV.


Interface - SENTINELA
---------------------

Administrar parâmetros de Risco

TODO - INICIAR


Aplicar parâmetros de Risco - OK

FEITO PROTO



Bases de Risco - Inteligência
-----------------------------

Ranquear Empresas

Como analista de dados, preciso dispor de uma série de relatórios
padronizados do DW que poderão ser rodados periodicamente
(semanalmente ou mensalmente). Estes relatórios trarão informações como
capital da Empresa, capital dos Sócios, idade dos sócios, idade da Empresa,
data de habilitação, tempo de habilitação, quantidade de despachantes,
ocorrências radar, etc. Um segundo momento agrupará e
transformará estes dados em dados categóricos para passar
em modelos de predição de risco.

Observação:

A ação acima deve implementar um pipeline facilmente reproduzível.
Pode ser agregado / assembled dados de importações, um ranking manual
(black-list), etc.
