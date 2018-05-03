`Voltar ao Indice <index.html>`_

=============================
Manual de Usuário do Virasana
=============================


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


.. _importa-bson:

-------------
Importar Bson
-------------
A tela Importar Base é onde se envia ao sistema os arquivos de imagem.

Ao lado do botão para enviar arquivo BSON contendo as imagens, é exibida uma pequena
lista dos últimos arquivos carregados no Servidor.

Esta tela só será utilizada em casos excepcionais. Os Avatares devem ser configurados
para enviar diretamente os arquivos bson via API. Se não houver comunicação entre a rede dos
da fontes de imagens (recinto) e o Servidor Virasana, o ideal é configurar uma task 
(ver :func: `virasana.virasana.workers.tasks.processa_bson`)
para varrer periodicamente um diretório de rede onde os arquivos bson sejam gravados
para importação automática pelo Virasana.

.. figure :: _static\\images\\importarbson.png
    :align: center

    Tela Importar Base

Para realizar o UPLOAD e submetê-lo ao sistema o usuário deverá:
    | Buscar o arquivo clicando em *BSON Gerado pelo AVATAR* e
      navegando até o local do arquivo.
    | Clicar em Submeter



.. _pesquisar-arquivos:

------------------
Pesquisar Arquivos
------------------
Nesta tela está a principal função do sistema, que consiste em navegar nos arquivos de imagens,
fazer filtragens, buscas e utilizar os algoritmos de aprendizagem de máquina.

É possível pesquisar por Número de Contêiner, período de escaneamento, e também exibir imagens
para as quais foi gerado alerta pelo Operador de Escâner.

Além destes, é possível criar filtros personalizados, por exemplo escolhendo campos do Sistema
Carga, na caixa "Selecione" abaixo da legenda "Definir filtro personalizado".

.. figure :: _static\\images\\pesquisar-arquivos.png
    :align: center

    Tela Pesquisar Arquivo


.. _ver-arquivo:

-----------
Ver Arquivo
-----------
Esta tela permite a visualização da imagem e de todas as informações vinculadas, divididas em abas.

A primeira aba mostra a imagem, o recorte do contâiner e um resumo das informações selecionadas. A seguir,
cada aba exibe informações detalhadas de cada base que tenha sido importada e vinculada com a imagem. Por
exemplo, normalmente as imagens de escaneamento possuem um XML vinculado, cujas informações serão exibidas
na segunda aba. Caso a imagem seja de um Contêiner controlado pelo sistema CARGA (modal marítimo), caso a
importação dos dados do sistema CARGA tenham sido importados e localizados com sucesso, esta informação
(Conhecimentos de transporte marítimo, Manifestos, NCMs, etc) estarão em uma aba.

.. figure :: _static\\images\\ver-arquivo.png
    :align: center

    Tela Ver Arquivo


.. _estatisticas:

------------
Estatísticas
------------

.. figure :: _static\\images\\estatisticas.png
    :align: center

Exibe números globais do Servidor em um período especificado: quantidade de imagens,
datas, problemas de integração, quantidade por recinto, variação ao longo do período, etc.

