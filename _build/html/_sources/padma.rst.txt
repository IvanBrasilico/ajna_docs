
.. contents:: Tópicos
 :depth: 2

`Voltar ao Indice <index.html>`_

=====
PADMA
=====
PADMA é o módulo responsável por servir e treinar os modelos de aprendizado de máquina


GYM
---
No diretório GYM estão os scripts de treinamento de modelos.

O treinamento da API TensorFlow é realizado em repositório próprio, separado(models.git).
É necessário clonar o repositório do TensorFlow Object Detection no raiz do Padma: 
https://github.com/IvanBrasilico/models

Usar Python3.5 e TensorFlow1.5
------------------------------
Atualmente o projeto TensorFlow models foi testado com o PADMA com:

- Python3.5 e TensorFlow1.5
- Python3.6 e TensorFlow1.4

O uso de Python3.6 e TensorFlow >=1.5 dá o erro no Atribute t.float32 in module TensorFlow


Interface
---------
.. automodule:: padma.padma.app
    :members:

Modelos
-------

.. automodule:: padma.padma.models.models
    :members:
.. automodule:: padma.padma.models.bbox.bbox
    :members:
.. automodule:: padma.padma.models.conteiner20e40.bbox
    :members:
.. automodule:: padma.padma.models.peso.peso
    :members:
.. automodule:: padma.padma.models.vazios.vazios
    :members:
