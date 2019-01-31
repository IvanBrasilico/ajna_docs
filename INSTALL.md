* [Módulos](#Módulos)
  * [Desenvolvimento](#Desenvolvimento)
  * [core](#Core)
  * [virasana](#virasana)
  * [bhadrasana](#bhadrasana)
  * [padma](#padma)

* [Estrutura]
`

# Módulos:

## Desenvolvimento
Recomenda-se, caso queira-se um ambiente para desenvolvimento, edição e geração de documentação
 clonar todos os repositórios dentro da pasta ajna.
 
Depois, dentro de cada pasta de cada módulo e com venv ativo, digitar:

```
(venv)$ ln -s ../commons/ajna_commons .
(venv)$ pip install -e .[dev]
```

## core
Core ou commons/docs. Contém as configurações para gerar documentação e as bibliotecas comnuns.
 
Este módulo. Requerido para todos os demais módulos AJNA.

Clonar o módulo raiz ajna e rodar install_*.sh no projeto ajna.


Automático:

```
$git clone https://github.com/IvanBrasilico/ajna.git
$cd ajna
$./install_requisites.sh
$./install_core.sh
```

Manual (presumindo que requisitos estão instalados e atualizados:

```
$git clone https://github.com/IvanBrasilico/ajna.git
$cd ajna
$python3 -m venv ajna-venv
$. ajna-venv/bin/activate
(ajna-venv)$pip install -e .[dev]
```


## virasana

Interface para visualização e busca de imagens.

Rodar install_virasana.sh no diretório raiz do ajna.

Ir para diretório virasana e rodar "./celery.sh" e "python wsgi_debug.py" para testar instalação. 

Rodar configure_virasana.sh para instalar as configurações do supervisor e do apache/nginx. Pode ser necessário
 editar os arquivos virasana/supervisor_* e revisar as configurações do apache/nginx manualmente para adaptar 
 ao ambiente utilizado. 

## bhadrasana

Controla o data_aq, permite cruzamento de dados e gerenciamento, manual ou automático, de parâmetros de risco.

A instalação segue exatamente os mesmos passos do virasana.

## padma

Coleção de algoritmos de machine learning plugáveis e servidos em WebService.

Rodar install_padma.sh no diretório raiz do ajna.

Ir para diretório padma e rodar "python modelserver.py" e "python wsgi_debug.py" para testar instalação. 

### Instalação manual 

```
$git clone <nome do repositório>
$cd <nome do módulo>
$python3 -m venv <modulo>-venv
$. <modulo>-venv/bin/activate
$pip install .
```
Ex:

```
$git clone https://github.com/IvanBrasilico/virasana.git
$cd virasana
$python3 -m venv virasana-venv
$. virasana-venv/bin/activate
(virasana-venv)$pip install .
(virasana-venv)$python -m pytest (roda os testes automatizados)
(virasana-venv)$./virasana/celery.sh (inicia os workers do serviço celery)
(virasana-venv)$ python virasana/app.py (inicia o servidor web/api)
```

### Desenvolvimento

A estrutura de diretórios ficará assim:

<pre>/ajna  
 ┬  
 ├  commons
 ├  bhadrasana
 ├  padma
 └  virasana
</pre>

Para poder editar o ajna_commons num local único (pois será instalada uma cópia em cada venv criado), dentro de cada diretório/módulo, com o venv respectivo ativo, digite:

```
$ pip uninstall ajna_commons
$ ln -s ../ajna_commons/ajna_commons .
```
