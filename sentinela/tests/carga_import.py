import csv
import importlib
import os

import pandas as pd

from sentinela.models.carga import Base, MySession

"""                                 Escala, AtracDesatracEscala, Manifesto,
                                    ManifestoConhecimento, Conhecimento,
                                    Container, CargaSolta, Granel, NCM)
"""
CARGA_BASE = '/home/ivan/pybr/AJNA_MOD/sentinela/CSV/1/2017/1221/'


mysession = MySession(Base, test=False)
session = mysession.session
engine = mysession.engine
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

files = sorted(os.listdir(CARGA_BASE))
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


dataframes = dfs
for csvf, df in dataframes.items():
    my_module = importlib.import_module('sentinela.models.carga')
    print('Iniciando import de ', csvf[:-4])
    try:
        MyClass = getattr(my_module, csvf[:-4])
        for i, row in df.iterrows():
            instance = MyClass()
            for campo in df.columns:
                try:
                    setattr(instance, campo, row[campo])
                    # afield = getattr(instance, campo)
                    # if not callable(afield):
                    #    afield = row[campo]
                except AttributeError:
                    pass
            print('**', instance)
            session.add(instance)
        session.commit()
    except AttributeError as err:
        print(err.args)
