"""Exemplo de utilização no sistema CARGA.
Teste funcional simulando utilização com uma base "real".
A base é uma base do Sistema Siscomex Carga modificada por questões de sigilo.
"""
import os
import tempfile
import unittest

from sentinela.models.models import (Base, Filtro, MySession, ParametroRisco,
                                     ValorParametro)
from sentinela.utils.csv_handlers import sch_processing
from sentinela.utils.gerente_risco import GerenteRisco

CARGA_ZIP_TEST = '/home/ivan/Downloads/P.zip'


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)
        self.tmpdir = tempfile.mkdtemp()
        # Ensure the file is read/write by the creator only
        self.saved_umask = os.umask(0o077)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        os.umask(self.saved_umask)

    def test_carga(self):
        # Define parâmetros de risco. Na interface de usuário estes
        # valores deverão estar persistidos em Banco de Dados e/ou serem
        # exportados ou importados via arquivo .csv
        # (GerenteRisco parametros_tocsv e parametros_fromcsv)
        #########################################################
        # Este precisa de uma extração disponível e é pesado
        # Para não rodar, renomeie o método para no_test_carga
        # O pytest só chama os métodos começados com test
        #
        ###################

        risco = ParametroRisco('CPFCNPJConsignatario', 'CNPJ do Consignatario')
        self.session.add(risco)
        # Adicionar um CNPJ que exista na extração, para testar...
        valor = ValorParametro('42581413000157', Filtro.igual)
        self.session.add(valor)
        risco.valores.append(valor)
        self.session.merge(risco)

        risco2 = ParametroRisco('DescricaoMercadoria', 'Descrição')
        self.session.add(risco2)
        # Adicionar uma mercadoria que exista na extração, para testar...
        valor2 = ValorParametro('PILLOW', Filtro.contem)
        self.session.add(valor2)
        self.session.commit()
        risco2.valores.append(valor2)
        self.session.merge(risco2)
        self.session.commit()
        # Comentado para não rodar no Servidor
        """filenames = sch_processing(CARGA_ZIP_TEST)
        print(filenames)
        assert not filenames is None
        # assert(len(filenames) == 14)
        gerente = GerenteRisco()
        gerente.add_risco(risco)
        print(risco.valores)
        with open(filenames[4][0]) as show_the_head:
            head = [next(show_the_head) for x in range(5)]
        print(head)
        result = gerente.aplica_risco(arquivo=filenames[4][0])
        print(result)
        # assert False  # To view output, uncomment this
        """
        # TODO:  Testar gerente.aplica_juncao() em uma base do Carga
