`Voltar ao Indice <index.html>`_

==============================
Manual de Usuário do Sentinela
==============================

Este será o manual de Usuário

Descreveremos a interface através de exemplos e imagens de telas

Fluxo de trabalho (Workflow)
============================

Após fazer o :ref:`login`, o usuário deverá ir à página :ref:`importa-base`
para cadastrar uma Base e selecionar o arquivo ao qual ele deseja realizar a
varredura de riscos. Após a importação será automaticamente redirecionado para
a tela de aplicação de riscos.

Na primeira vez em que uma base for cadastrada será necessário configurar os
parâmetros de risco. A tela :ref:`edita-risco` apresenta exatamente esta
função.


Observação:
    A criação e/ou edição dos parâmetros de riscos, serão realizadas somente
    na primeira vez em que ele cadastrar uma nova Base.


Telas
=====

.. _login:

Login
-----

Esta é a tela inicial do sistema Sentinela. Ao entrar será solicitado login
e senha.

.. image :: _static\\images\\login.png
    :target: ..\index.html

Após entrar o sistema apresentará a página Home.

.. _importa-base:

Importar Base
-------------

A tela Importar Base é onde se envia o arquivo que se deseja filtrar para o sistema.

.. image :: _static\\images\\importarbase.png
    :target: ..\index.html

Nesta tela encontramos os seguintes campos:
 - Seleção de arquivos
 - Seleção **ou** cadastramento de bases
 - Data do período da extração


.. _aplica-risco:

Aplicar Risco
-------------

Para aplicar o risco no arquivo importado basta selecionar os parâmetros
definidos na tela :ref:`edita-risco` a serem filtrados na planilha e,
após isso selecionar **Filtrar**. Será apresentada uma tabela contendo os
campos e as linhas as quais foram encontrados os riscos definidos.

.. image :: _static\\images\\aplicarrisco.png
    :target: ..\index.html

Nesta tela encontramos os seguintes campos:
 - Seleção da Base
 - Modo de visualização
 - Seleção do padrão de risco
 - Parâmetros ativos cadastrados na tela :ref:`edita-risco`


.. _edita-risco:

Editar Riscos
-------------
Esta tela permite a edição e/ou cadastro de parâmetros de risco.


.. image :: _static\\images\\editarrisco.png
    :target: ..\index.html


Nesta tela encontramos os seguintes campos:
 - Seleção/criação do padrão de risco
 - Seleção das bases a serem vinculadas
 - Cadastramento dos parâmetros
 - Cadastramento dos valores dos parâmetros

Ao clicar na lupa ao lado do campo de cadastro de parâmetros o sistema buscará
os titulos das colunas já importados.


.. _edita-titulos:

Editar Titulos
--------------

