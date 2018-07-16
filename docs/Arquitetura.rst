`Voltar ao Indice <../index.html>`_


.. contents:: Tópicos
 :depth: 2


==================
Módulos do Sistema
==================

AVATAR
======
Interface para cadastramento de fontes de imagens, usuários, configuração de parâmetros, etc
Podem existir várias versões do AVATAR, de acordo com a necessidade (para diferentes portos,
aeroportos, remessa expressa, etc)

image_aq
--------

Serviço interno do AVATAR.
Aquisição de imagens. Serviço com Scripts que acessam as fontes de imagens cadastradas,
validam, pré-processam, fazem reconhecimento de caracteres, validam,
monitoram mudanças, etc e copiam para um diretório único.

As imagens são arquivadas em diretório no formato <Nome_da_Fonte_de_Imagens>/<Ano>/<Mes>/<dia>.
Se possível, será armazenada a imagem original. No mínimo será armazenada uma cópia em menor resolução
(e sem outras transformações) da imagem original, além dos metadados (xml original ou outro).
Deve ser provida uma forma de proteger contra modificações (read-only).

Exporta seus dados em lotes para arquivo BSON.

BHADRASANA
==========

Aquisição de dados. Serviço com scripts que acessam sistemas fechados e dados públicos,
estruturados e não estruturados, guardando em coleções/Bancos de Dados.

Os dados são arquivadas em diretório no formato <Nome_da_Base_Original>/<Ano>/<Mes>/<dia>/<Codigo_Extracao>
A BaseOriginal será armazenada em csv no padrão cabeçalho na primeira linha com nomes dos campos,
separador vírgula, e somente isso(rfc4180 - forma mais simples). As "Strings" originais dos dados terão sempre
os espaços à direita e esquerda removidas e serão normalizados para Unicode NFC sem acentos e caracteres especiais,
com espaços únicos entre as palavras e letras minúsculas. Todos os dados originais serão tratados como Strings. Estas
precauções servirão para facilitar buscas, comparações e evitar problemas de codificação e compatibilidade
futuras e em interações com outros sistemas.

Os Dados importados são arquivados em um banco MongoDB, no formato original do CSV

Sentinela
---------

Interface gráfica do BHADRASANA.

Controla o BHADRASANA, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco.

Interface para cadastramento e configuração das Fontes de Dados(Configura modo de merge entre as tabelas originais,
filtragens, etc)

Estas configurações permitirão a migração automática, se necessário, dos dados dos CSV originais para MongoDB

Quando o sistema original não permitir sincronização/extração automática, sentinela proverá interface para
alimentação manual da base.

Disponibiliza seus dados em Restful API.

VIRASANA
========

Banco de Dados de imagens.

Importa arquivos BSON dos AVATARES.

Submódulo integração provê, para cada Fonte de Dados, scripts para ETL (Extração, Transformação e 'LOAD'),
com heurísticas para adicionar aos metadados das imagens os dados das Fontes de Dados e análises do PADMA.

Serviço Celery rodará periodicamente a importação de imagens de BSON e a anexação de metadados.

Provê também interface para visualização e busca de imagens e execução,
manual ou automática, dos algoritmos do módulo PADMA nas imagens.

Serviço também de auditoria, cruzando dados das diversas fontes.

Disponibiliza seus dados em Restful API.


PADMA
=====

Coleção de algoritmos de machine learning plugáveis e servidos em WebService/JSON API.

notebooks/scripts
-----------------

Rascunhos. Aproveitar a interatividade e praticidade do Jupyter Notebook/JupyterLab
para fazer e documentar as análises exploratórias de dados,
treinamento e teste de algoritmos de aprendizado de máquina.

.. _Arquitetura:

======================
Arquitetura do Sistema
======================

Descrição do 'Pipeline' básico
==============================

Importação
----------
A importação de dados imagens poderá ser realizada por serviços(caso A), caso possível por senha, token
ou certificado digital de Servidor extrair informações periodicamente dos sistemas externos necessários.

Caso o acesso ao Sistema Fonnte de dados necessite de digitação manual de senha,
Usuário(caso B) realizará uma extração manual periódica.

No caso de importação das imagens, pode haver redes de dados incomunicáveis. Assim, o Avatar terá que
exportar para um arquivo e após, algum Usuário do sistema precisará colocar estes arquivos em uma pasta
à qual o Virasana tenha acesso. Havendo comunicação de rede, o Avatar deve ser configurado para fazer
UPLOAD diretamente via API do Virasana sempre que fechar um lote.

Idealmente os dados e imagens recebidos ficarão guardados no formato original do Sistema.


Obs: Estes sistemas fonte de dados precisarão estar documentados/listados em rotinas de trabalho (caso B) ou em
configuração do sistema (caso A).

No caso A, um serviço mestre utilizará esta lista de serviços para detectar serviços não funcionando e alertar.
Um serviço de log mestre deve permitir acompanhar o histórico de importações, e se há sucesso ou falha.

Esta camada será executada por serviços Celery

Ex.:

* bhadrasana conectando aos sistemas dos terminais

* virasana capturando imagens conforme disponibilizadas

* Usuário fazendo extração do Siscomex Carga e carregando em interface do bhadrasana

* Usuário fazendo upload de novas imagem em interface do virasana

* Integração automática com Aniita ou Contágil


Pré-processamento
-----------------

Uma segunda camada irá  processar previamente os dados e colocá-los em formato mais
amigável para integração com as etapas seguintes.
Serão "normalizados" campos, pré-indexadas imagens, descompactados arquivos,
checar integridade, etc.

Esta camada será executada por um segundo serviço Celery rodando no Servidor Bhadrasana
Serão utilizadas bases/funcões de outros módulos, mas serão executados por este módulo.

Este módulo não tem interface de usuário.
Todas as ações configuráveis são pré-programadas no bhadrasana ou no virasana.
Algumas ações serão "hard-coded".

Ex.:

* bhadrasana mudando títulos de csvs de diferentes terminais mas que possuem as mesmas informações.

* bhadrasana usando o módulo ajna_commons.utils.sanitizar para corrigir textos e facilitar pesquisas,
    colocando tudo em caixa única, retirando sinais gráficos e espaços duplicados, etc.


Integração
----------

Módulo integração será desenvolvido no Virasana. Para cada base de dados disponível, scripts adicionarão
as informações mais importantes desta diretamente à base de imagens, para consultas e cruzamento.

Checagens de segurança
----------------------

Esta camada estará integrada no módulo virasana ou no próprio módulo Avatar.
Serão feitas análises básicas e emitidos alertas.


Exemplo:

*  Foi gerada nova imagem para contêiner já escaneado? É igual? Data do sistema de controle de escaneamentos bate com a da imagem?

*  OCR da imagem bate com número do contêiner informado no XML?

*  Foi retificada informação de Sistema já importada?


Análises de Risco
-----------------

Poderão ser automáticas ou manuais. Realizadas e configuradas no sistema bhadrasana, conforme manual.

As automáticas serão executadas pelo Celery do Servidor Bhadrasana.


Análises de Risco "Inteligentes"
--------------------------------

O Virasana, após receber as imagens e fazer a integração dos dados, realizará automaticamente consulas ao PADMA,
bem como cruzamento de dados, gerando alertas para as inconsistências.

* virasana fazendo miniatura das imagens e gerando índice destas

* virasana fazendo checagem de vazios

* virasana validando peso e volume da imagem e comparando com dados documentais e de balança

* virasana passa módulo de procura de drogas e armas em novas imagens


Notas gerais sobre implementação
--------------------------------

Esta seção se dedica a anotações sobre a real implementação da Arquitetura conforme os desenvolvimentos avançam.


O Avatar da ALFSTS foi desenvolvido em Python/Django com banco SQlite.

O Virasana está em Python/Flask e o seu BackEnd (banco de imagens) em MongoDB. Processos demorados rodam via Celery e se
comunicam com o processo principal, se necessário, via REDIS.

O Bhadrasana está em Python/Flask e guarda as importações originais diretamente no filesystem em formato texto/csv RFC padrão
e utiliza o BackEnd do Virasana para "arquivamento"/exportação destas extrações.
Possui também BD de configuração interno em SQlite.  Processos demorados rodam via Celery e se
comunicam com o processo principal, se necessário, via REDIS.

O Padma utiliza Sklearn e TensorFlow para os modelos. Para o Front-end, Python e Flask. Há um processo separado para servir os
modelos que se comunica com o Servidor WEB/API via REDIS.