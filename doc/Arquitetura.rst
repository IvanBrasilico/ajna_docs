`Voltar ao Indice <../index.html>`_

======================
Arquitetura do Sistema
======================

.. contents:: Tópicos
 :depth: 2

Descrição do 'Pipeline' básico
==============================

Importação
----------
Serviços(A) - caso possível por senha, token ou certificado digital de Servidor - extraem informações periodicamente de diversos sistemas. Estes ficam originalmente no formato original do Sistema. Caso o Sistema fonte necessite de digitação manual de senha, Usuário(B) iniciará a extração manual.

Obs: Estes sistemas fonte de dados precisarão estar documentados/listados e em rotinas de trabalho (caso B). Um serviço mestre utilizará esta lista de serviços para detectar serviços não funcionando e alertar. Um serviço de log mestre deve permitir acompanhar o histórico de importações, e se há sucesso ou falha.

Esta camada provavelmente será executada por um serviço Celery

Ex.:

* data_aq conectando aos sistemas dos terminais

* img_aq capturando imagens conforme disponibilizadas

* Usuário fazendo extração do Siscomex Carga em interface do data_aq

* Usuário informando nova imagem em interface do img_aq

* Integração automática com Aniita ou Contágil


Pré-processamento
-----------------

Uma segunda camada irá  processar previamente os dados e colocá-los em formato mais amigável para integração com as etapas seguintes. Serão "normalizados" campos, pré-indexadas imagens, descompactados arquivos, checar integridade, etc.

Esta camada provavelmente será executada por um segundo serviço Celery. Serão utilizadas bases/funcões de outros módulos, mas serão executados por este módulo.

Este módulo não tem interface de usuário. Todas as ações configuráveis são pré-programadas no SENTINELA ou no CHAKRA. Algumas ações serão "hard-coded".

Ex.:

* CHAKRA fazendo miniatura das imagens e gerando índice destas

* SENTINELA mudando títulos de csvs de diferentes terminais mas que possuem as mesmas informações.



Checagens de segurança
----------------------

Esta camada provavelmente estará integrada na Segunda. Serão feitas análises básicas e emitidos alertas.


Exemplo:

*  Foi gerada nova imagem para contêiner já escaneado? É igual? Data do sistema de controle de escaneamentos bate com a da imagem?

*  OCR da imagem bate com número do contêiner informado no XML?

*  Foi retificada informação de Sistema já importada?




Análises de Risco
-----------------

Poderão ser automáticas ou manuais
