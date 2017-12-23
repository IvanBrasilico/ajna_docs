import csv
import datetime
import importlib
import os

import pandas as pd

from sentinela.app import CSV_FOLDER
from sentinela.models.carga import Base, MySession

CARGA_BASE = os.path.join(CSV_FOLDER, '1/2017/1221/')

mysession = MySession(Base, test=True)
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
            if ind > MAX_LINES:
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
                    val = row[campo]
                    pos_parenteses = campo.find('(')
                    if pos_parenteses != -1:
                        campo = campo[:pos_parenteses]
                    if campo in instance.__table__.c:
                        ctype = instance.__table__.c[campo].type
                        if str(ctype) == 'NUMERIC':
                            val = val.replace(',', '.')
                        elif str(ctype) == 'DATETIME':
                            if val:
                                val = datetime.datetime.strptime(
                                    val, '%d/%m/%Y').date()
                            else:
                                val = None
                        setattr(instance, campo, val)
                except AttributeError:
                    pass
            session.add(instance)
        print(i, ' registros importados')
        session.commit()
    except AttributeError as err:
        print(err.args)
