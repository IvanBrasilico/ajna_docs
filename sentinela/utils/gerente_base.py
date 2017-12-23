"""GerenteBase abstrai a necessidade de conhecer a estrutura das bases
ou utilizar comandos mais avançados. Transforma a estrutura em dicts
mais fáceis de lidar"""
import csv
import importlib
import inspect
import os
from collections import defaultdict

from sentinela.conf import APP_PATH, CSV_FOLDER

PATH_MODULOS = os.path.join(APP_PATH, 'models')


class GerenteBase:
    """Métodos para padronizar a manipulação de bases de dados
     no modelo do sistema sentinela"""

    def set_path(self, path):
        """Lê a estrutura de 'tabelas' de uma pasta de csvs importados"""
        PATH_BASE = os.path.join(CSV_FOLDER, path)
        files = sorted(os.listdir(PATH_BASE))
        self.dict_models = defaultdict(dict)
        for file in files:
            with open(os.path.join(PATH_BASE, file), 'r',
                      encoding='latin1', newline='') as arq:
                reader = csv.reader(arq)
                cabecalhos = next(reader)
                campos = [campo for campo in cabecalhos]
                self.dict_models[file[:-4]]['campos'] = campos

    def set_module(self, model):
        """Lê a estrutura de 'tabelas' de um módulo SQLAlchemy"""
        module_path = 'sentinela.models.' + model
        module = importlib.import_module(module_path)
        classes = inspect.getmembers(module, inspect.isclass)
        self.dict_models = defaultdict(dict)
        for i, classe in classes:
            print(classe.__name__)
            if classe.__name__:
                campos = [i for i in classe.__dict__.keys() if i[:1] != '_']
                self.dict_models[classe.__name__]['campos'] = sorted(campos)

    @property
    def list_models(self):
        if self.dict_models is None:
            return None
        return self.dict_models.keys()

    @property
    def list_modulos(self):
        lista = [filename[:-3] for filename in os.listdir(PATH_MODULOS)
                if filename.find('.py') != -1]
        return sorted(lista)
