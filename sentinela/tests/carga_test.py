import csv
import importlib
import os
import unittest

import pandas as pd

from sentinela.models.carga import Base, Escala, MySession

CARGA_BASE = 'sentinela/tests/CSV/1/2017/0329/'


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def open_csvs(self, path):
        files = sorted(os.listdir(path))
        dfs = {}
        for r in range(len(files)):
            with open(os.path.join(CARGA_BASE, files[r]), 'r',
                      encoding='latin1', newline='') as arq:
                reader = csv.reader(arq)
                MAX_LINES = 10
                lista = []
                for ind, linha in enumerate(reader):
                    lista.append(linha)
                    if ind == MAX_LINES:
                        break
            df = pd.DataFrame(lista[1:], columns=lista[0])
            dfs[files[r]] = df
        return dfs

    def test_escala(self):
        escala = Escala()
        escala.Escala = '000000'
        self.session.add(escala)
        self.session.commit()
        self.carga_import()

    def carga_import(self):
        dataframes = self.open_csvs(CARGA_BASE)
        for csvf, df in dataframes.items():
            my_module = importlib.import_module('sentinela.models.carga')
            try:
                MyClass = getattr(my_module, csvf[:-4])
                for i, row in df.iterrows():
                    instance = MyClass()
                    for campo in df.columns:
                        afield = getattr(instance, campo)
                        if not callable(afield):
                            afield = row[campo]
                    self.session.add(instance)
            except AttributeError as err:
                print(err.args)
        self.session.commit()
