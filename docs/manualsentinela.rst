`Voltar ao Indice <index.html>`_

===============================
Manual de Usuário do Bhadrasana
===============================

Descrevemos a interface através de exemplos e imagens de telas.

Fluxo de trabalho (Workflow)
============================

Para começar a utilizar o sistema, o usuário, após efetuar o :ref:`login`,
deverá ir à página :ref:`importa-base` para cadastrar/selecionar uma Base e
importar o arquivo ao qual ele deseja realizar a busca por elementos de risco.
Após a importação será automaticamente redirecionado para a tela :ref:`aplica-risco`.

Na primeira vez em que uma Base for cadastrada será necessário criar os itens
de riscos que serão buscados. A tela :ref:`edita-risco` apresenta a função de
criação e edição destes Padrões de Risco.

Após a criação dos padrões o usuário poderá realizar a filtragem da Base desejada
indo na tela :ref:`aplica-risco` e selecionando os itens necessários.

O Sentinela (ver :doc:`bhadrasana`) já na importação aplica alguns filtros e
normalizações na Base importada.

Caso existam várias bases com parâmetros parecidos, diferindo apenas no nome, o
sistema apresenta na tela :ref:`edita-titulo` um mecanismo para igualar o nome
dos parâmetros destas planilhas.

.. important :: A troca de títulos será feita apenas ao importar a Base.
    Ver :ref:`edita-titulo` para mais informações.

Telas
=====

.. _login:

-----
Login
-----
Esta é a tela inicial padrão do sistema AJNA.
Nela está contido o formulário de login.

.. figure :: _static\\images\\login.png
    :align: center

    Tela Login


.. _importa-base:

-------------
Importar Base
-------------
A tela Importar Base é onde se envia ao sistema os arquivos para que sejam
aplicados os filtros.

.. figure :: _static\\images\\importarbase.png
    :align: center

    Tela Importar Base

Para realizar o UPLOAD e submetê-lo ao sistema o usuário deverá:
    | Buscar o arquivo clicando em *Clique para selecionar planilha* e
      navegando até o local do arquivo.
    | Escolher a Base Original. Caso ela ainda não tenha sido criada,
      digitar o nome no campo *Nome* e clicar em *Criar nova Base de Origem*.
    | Escolher a data do arquivo. Caso nada seja digitado será atribuído a
      data atual a este campo

Após clicar em *Submeter* o sistema redirecionará para a tela :ref:`aplica-risco`.
Porém se não houver Padrão de Risco cadastrado o usuário deverá ir para a página
:ref:`edita-risco`.

.. important :: Os arquivos importados deverão ter os formatos: CSV (Arquivo
    de texto delimitado por vírgulas), SCH - TXT, ZIP (Contendo arquivos CSV
    ou SCH-TXT)

.. _aplica-risco:

-------------
Aplicar Risco
-------------
Nesta tela está a principal função do sistema, que consiste em verificar se há
parâmetros de risco nas Bases.

.. figure :: _static\\images\\aplicarrisco.png
    :align: center

    Tela Aplicar Risco

Para aplicar o risco no arquivo importado:
    | Escolher o Padrão de Risco, já configurado na tela :ref:`edita-risco`
    | Selecionar os parâmetros que serão aplicados à Base desejada
    | Selecionar o modo de visualização (ver :ref:`edita-visao`)

Após clicar em selecionar *Filtrar*. O sistema apresentará uma tabela contendo
os campos e as linhas as quais foram encontrados os valores definidos.

Apresenta os seguintes campos:
 - Seleção da Base
 - Modo de visualização
 - Seleção do padrão de risco
 - Parâmetros ativos cadastrados na tela :ref:`edita-risco`


.. _edita-risco:

-------------
Editar Riscos
-------------
Esta tela permite a edição e/ou cadastro dos Padrões de Risco.

.. figure :: _static\\images\\editarrisco.png
    :align: center

    Tela Editar Riscos

Estes padrões consistem nas colunas dos arquivos importados, a qual chamaremos 
de parâmetros, e seus respectivos valores. Como mostra a figura abaixo.

.. figure :: _static\\images\\padrao.png
    :align: center

    Exemplificando os parâmetros e seus valores

Apresenta os seguintes campos:
 - Seleção/criação do padrão de risco
 - Seleção das bases a serem vinculadas
 - Cadastramento dos parâmetros
 - Cadastramento dos valores dos parâmetros

.. tip :: Ao clicar na lupa ao lado do campo de cadastro de parâmetros o
    sistema buscará os titulos das colunas de arquivos já importados.

.. note :: A criação dos padrões de riscos, serão realizadas somente na
    primeira vez em que for cadastrado uma nova Base.


.. _edita-titulo:

--------------
Editar Titulos
--------------

.. figure :: _static\\images\\editatitulo.png
    :align: center

Para casos onde há mais de uma Base, alguns parâmetros poderão estar com nomes
diferentes, porém, trazerem os mesmos valores como, por exemplo:

.. figure :: _static\\images\\plan1.png
    :align: center

    Planilha 1

.. figure :: _static\\images\\plan2.png
    :align: center

    Planilha 2

Se, no exemplo dado, as colunas das planilhas tivessem um único nome (já que
ambas trazem o código NCM) poderia ser cadastrado um único parâmetro onde nele
seriam cadastrados todos os códigos de NCMs desejados.

Ao invés de criar um Parâmetro de Risco diferente para cada Base (ver
:ref:`edita-risco`), nesta tela o Sentinela permite que uma coluna seja
importada com um outro nome.

Por exemplo:
    Supondo que quisessemos padronizar os nomes dos campos para **NCM** somente,
    deveríamos mudar o nome *Código NCM* da Planilha 1 para *NCM*
    da Planilha 2.
    
    Para isso basta colocar o título que queremos que seja trocado no campo
    *Título antigo*, e o título novo no campo *Título novo*.

    .. figure :: _static\\images\\editatituloex.png
        :align: center

        Exemplo da mudança de título

    E na tela :ref:`edita-risco` criamos um único parâmetro como na figura
    abaixo.

    .. figure :: _static\\images\\editariscoex.png
        :align: center

        Exemplo de parâmetro de risco

.. caution :: O sistema só realizará as trocas de títulos no momento em que o
    arquivo estiver sendo importado. Ou seja, o procedimento para padronização
    dos títulos deverão ser configurados antes do UPLOAD da Base na tela 
    :ref:`importa-base`



.. _edita-visao:

--------------
Editar Visão
--------------
Esta tela permite ao usuário definir quais colunas exibir na tela :ref:`aplica-risco`.