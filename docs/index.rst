.. AJNA documentation master file, created by
   sphinx-quickstart on Tue Nov 14 11:22:53 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Introdução
==========

Bem-vindo à documentação do sistema AJNA
----------------------------------------

AJNA - Visão computacional e Aprendizagem de máquina aplicados à vigilância aduaneira
-------------------------------------------------------------------------------------

AJNA é, na tradição do Ioga, o chakra da intuição, ou terceiro olho.

Ioga é a melhoria pessoal através da prática, pode ser traduzido simplesmente por prática.

O nome AJNA dado ao sistema de vigilância aduaneira com auxílio de inteligência
artificial simboliza isso: prática visando obter uma visão mais plena.

O AJNA, para diminuir sua complexidade e facilitar o desenvolvimento e manutenção, foi
repartido em módulos: 

AVATAR - Sistema que roda no ambiente dos recintos aduaneiros, gerenciando a aquisição das imagens
no ambiente original - podem existir vários AVATARES, desenvolvidos pela RFB ou pelos intervenientes
de acordo com as especificações da RFB. Os AVATARES atuam no mundo "físico" dos recintos, capturando
imagens, vídeos, e fazendo pequenas auditorias/verificações, para posterior envio ao sistema centralizado

VIRASANA - Sistema que roda no ambiente da RFB, recebendo pacotes de dados do sistema AVATAR.
Após receber as imagens, roda diversos scripts de integração, utilizando dados recebidos pelos módulos
AVATAR, BHADRASANA e PADMA.
Virasana representa a prática da postura do Herói, estar atento às informações para agir.

BHADRASANA - Sistema que roda no ambiente da RFB, importando dados de outros sistemas. Permite também
fazer pequenas navegações de dados e análise de risco.
Bhadrasana representa a prática da postura de meditação, observar, analisar.

PADMA - módulo responsável por servir e treinar os modelos de aprendizado de máquina
Padma representa a busca da verdade

Tópicos
=======
.. toctree::
   :maxdepth: 2
   :caption: Tópicos:
   :glob:

   manuais.rst
   codigofonte.rst
   UserStories.rst
   Arquitetura.rst
   modules.rst


Índices e tabelas
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
