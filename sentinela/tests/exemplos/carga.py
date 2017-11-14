"""Exemplo de utilização no sistema CARGA.
Teste funcional simulando utilização com uma base "real".
A base é uma base do Sistema Siscomex Carga modificada por questões de sigilo.
"""
import unittest

from sentinela.models.models import (Base, Filtro, MySession, ParametroRisco,
                                     ValorParametro)
from sentinela.utils.csv_handlers import sch_processing
from sentinela.utils.gerente_risco import GerenteRisco

CARGA_ZIP_TEST = '/home/ivan/Downloads/P1.zip'


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_carga(self):
        # Define parâmetros de risco. Na interface de usuário estes
        # valores deverão estar persistidos em Banco de Dados e/ou serem
        # exportados ou importados via arquivo .csv
        # (GerenteRisco parametros_tocsv e parametros_fromcsv)

        risco = ParametroRisco('teste', 'CNPJ do Consignatario')
        self.session.add(risco)
        valor = ValorParametro('00000000000001', Filtro.igual)
        self.session.add(valor)
        self.session.commit()
        risco.valores.append(valor)
        self.session.merge(risco)
        self.session.commit()
        filenames = sch_processing(CARGA_ZIP_TEST)
        print(filenames)
        assert(len(filenames) == 14)
        gerente = GerenteRisco()
        gerente.add_risco(risco)
        result = gerente.aplica_risco(arquivo=filenames[1][0])
        print(result)
        assert False  # To view output, uncomment this
