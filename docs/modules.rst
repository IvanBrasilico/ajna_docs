`Voltar ao Indice <index.html>`_

==================
Módulos do Sistema
==================

AJNA - Visão computacional e aprendizado de máquina

admin_interface
---------------

Interface para cadastramento de fontes de imagens, usuários, configuração de parâmetros, etc

image_aq
--------

Aquisição de imagens. Serviço com Scripts que acessam as fontes de imagens cadastradas,
validam, pré-processam, fazem reconhecimento de caracteres, validam,
monitoram mudanças, etc e copiam para um diretório único.

As imagens são arquivadas em diretório no formato <Nome_da_Fonte_de_Dados>/<Ano>/<Mes>/<dia>.
Se possível, será armazenada a imagem original. No mínimo será armazenada uma cópia em menor resolução
(e sem outras transformações) da imagem original, além dos metadados (xml original ou outro), e as
transformações, como imagem tratada para algoritmo de aprendizado, histograma extraído, etc.
Deve ser provida uma forma de proteger contra modificações (read-only).


Disponibiliza seus dados em Restful API.

data_aq
-------

Aquisição de dados. Serviço com scripts que acessam sistemas fechados e dados públicos,
estruturados e não estruturados, guardando em coleções/Bancos de Dados.

Os dados são arquivadas em diretório no formato <Nome_da_Base_Original>/<Ano>/<Mes>/<dia>/<Codigo_Extracao>
A BaseOriginal será armazenada em csv no padrão cabeçalho na primeira linha com nomes dos campos,
separador vírgula, e somente isso(rfc4180 - forma mais simples). As "Strings" originais dos dados terão sempre
os espaços à direita e esquerda removidas e serão normalizados para Unicode NFC sem acentos e caracteres especiais,
com espaços únicos entre as palavras e letras minúsculas. Todos os dados originais serão tratados como Strings. Estas
precauções servirão para facilitar buscas, comparações e evitar problemas de codificação e compatibilidade
futuras e em interações com outros sistemas.

Deve ser provida uma forma de proteger contra modificações (read-only).

Disponibiliza seus dados em Restful API.

sentinela
---------

Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco.

Interface para cadastramento e configuração das Fontes de Dados(Configura modo de merge entre as tabelas originais,
filtragens, etc)

Estas configurações permitirão a migração automática, se necessário, dos dados dos CSV originais para BDs SQL ou
NoSQL (a definir / enquanto dados não tiverem DataLake).

Quando o sistema original não permitir sincronização/extração automática, sentinela proverá interface para
alimentação manual da base.

Disponibiliza seus dados em Restful API.

chakra
------

Interface para visualização e busca de imagens, recebimento de alertas e execução,
manual ou automática, dos algoritmos do módulo ml_code nas imagens.

Disponibiliza seus dados em Restful API.

ml_code
-------

Coleção de algoritmos de machine learning plugáveis e servidos em WebService/JSON API.

notebooks
---------

Rascunhos. Aproveitar a interatividade e praticidade do Jupyter Notebook/JupyterLab
para fazer e documentar as análises exploratórias de dados,
treinamento e teste de algoritmos de aprendizado e projetar/validar scripts de data_aq.
