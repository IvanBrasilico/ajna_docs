
.. contents:: Tópicos
 :depth: 3

`Voltar ao Indice <index.html>`_

========
VIRASANA
========
Virasana é o módulo que recebe as imagens dos AVATARES, permite gerenciar e consultar as
imagens, e busca completar as imagens com metadados vindos dos módulos BHADRASANA e PADMA


Interface
=========
.. automodule:: virasana.virasana.views
    :members:


Integracao
==========
Neste diretório ficam os diversos scripts para integração entre as imagens e 
as fontes de dados. Cada fonte de dados deve ter um módulo definido.

__init__
--------
.. automodule:: virasana.virasana.integracao
    :members:

XML
-----
.. automodule:: virasana.virasana.integracao.xmli
    :members:

Carga
-----
.. automodule:: virasana.virasana.integracao.carga
    :members:

Workers
========

dir_monitor
-----------
.. automodule:: virasana.virasana.workers.dir_monitor
    :members:

tasks
-----
.. automodule:: virasana.virasana.workers.tasks
    :members:
