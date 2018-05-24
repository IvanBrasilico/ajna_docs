
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


Scripts
=======
Este módulo possui scripts utilizados para rodar tarefas de integração e manutenção da base
de dados. Normalmente os scripts utilizam funções do módulo integração.
A integração é parte do pipeline (Ver :ref:`Arquitetura`), e normalmente será chamada
periodicamente pelos :ref:workers. e :ref:tasks. Muitos scripts são para ajustes quando os
workers falharem e/ou para testes e integrações off-line.

Carga
-----
.. automodule:: virasana.virasana.scripts.cargaupdate
    :members:

XML
-----
.. automodule:: virasana.virasana.scripts.xmlupdate
    :members:

Predições (PADMA)
-----------------
.. automodule:: virasana.virasana.scripts.predictionsupdate
    :members:


Integracao
==========
Neste módulo ficam os diversos scripts para integração entre as imagens e 
as fontes de dados. Cada fonte de dados deve ter um módulo definido.

__init__
--------
.. automodule:: virasana.virasana.integracao
    :members:

Carga
-----
.. automodule:: virasana.virasana.integracao.carga
    :members:

.. _workers:

XML
-----
.. automodule:: virasana.virasana.integracao.xmli
    :members:

Workers
========

dir_monitor
-----------
.. automodule:: virasana.virasana.workers.dir_monitor
    :members:

.. _tasks:

Tasks
-----
.. automodule:: virasana.virasana.workers.tasks
    :members:
