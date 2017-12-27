"""Exemplo de utilização no sistema COV.
Teste funcional simulando utilização com uma base "real".
"""
import os
import tempfile
import unittest

from sentinela.models.models import (Base, BaseOrigem, DePara, MySession,
                                     PadraoRisco)
from sentinela.utils.csv_handlers import muda_titulos_csv, muda_titulos_lista
from sentinela.utils.gerente_risco import GerenteRisco

PLANILHA_TEST = ('/Users/47020753817/Downloads/WinPython-64bit-3.5.3.1Qt5'
                 '/notebooks/btp 5 setembro.csv')
CSV_NAMEDRISCO_TEST = 'sentinela/tests/csv_namedrisco_example.csv'
CSV_TITLES_TEST = 'sentinela/tests/BTP.csv'
CSV_MATRIZRISCO_TEST = ('/Users/47020753817/Downloads/'
                        'WinPython-64bit-3.5.3.1Qt5/'
                        'notebooks/Matriz Risco.csv')


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

    def test_planilhas(self):
        gerente = GerenteRisco()
        gerente.import_named_csv(CSV_NAMEDRISCO_TEST)
        gerente.parametros_tocsv(self.tmpdir)  # path='.')
        gerente.clear_risco()
        gerente.parametros_fromcsv('alimento', path=self.tmpdir)
        # , path='.')

    def test_planilhas_BD(self):
        gerente = GerenteRisco()
        gerente.import_named_csv(CSV_NAMEDRISCO_TEST, self.session)
        gerente.parametros_tocsv(self.tmpdir)  # path='.')
        gerente.clear_risco()
        gerente.parametros_fromcsv('alimento', path=self.tmpdir)
        # , path='.')

    def test_planilhaCOV(self):
        base = BaseOrigem('Planilha_BTP')
        self.session.add(base)
        self.session.commit()
        depara1 = DePara('nome motorista', 'nomemotorista', base)
        self.session.add(depara1)
        depara2 = DePara('cpf motorista', 'cpfmotorista', base)
        self.session.add(depara2)
        depara3 = DePara('descricao ncm', 'mercadoria', base)
        self.session.add(depara3)
        depara4 = DePara('razao social exportador / importador',
                         'nomeexportador', base)
        self.session.add(depara4)
        depara5 = DePara('cnpj exportador / importador',
                         'cnpjexportador', base)
        self.session.add(depara5)
        depara6 = DePara('nome operador scanner', 'operadorscanner', base)
        self.session.add(depara6)
        depara7 = DePara('cpf operador scanner', 'cpfoperadorscanner', base)
        self.session.add(depara7)
        depara9 = DePara('cnpj transportadora', 'cnpjtransportadora', base)
        self.session.add(depara9)
        self.session.commit()
        de_para_dict = {
            depara.titulo_ant: depara.titulo_novo for depara in base.deparas}
        print(de_para_dict)
        # TODO: Fazer planilha COV "FAKE" com títulos reais
        # e linha de dados
        lista_nova = muda_titulos_csv(CSV_TITLES_TEST, de_para_dict)
        lista_old = [['nome motorista', 'cpf motorista', 'descricao ncm',
                      'razao social exportador / importador',
                      'cnpj exportador / importador',
                      'nome operador scanner', 'cpf operador scanner',
                      'cnpj transportadora'], ['dado1c1', 'dado1c2']]
        lista = muda_titulos_lista(lista_old, de_para_dict)
        print(lista_nova[0])
        print('lista')
        print(lista[0])
        for old, new in de_para_dict.items():
            assert old in ''.join(lista_old[0])
            assert new not in ''.join(lista_old[0])
        for old, new in de_para_dict.items():
            assert new in ''.join(lista_nova[0])
        padraorisco = PadraoRisco('PlanilhaCOV')
        self.session.add(padraorisco)
        self.session.commit()
        # gerente = GerenteRisco()
        # gerente.import_named_csv(CSV_MATRIZRISCO_TEST, session=self.session,
        #                         padraorisco=padraorisco)
        # lista_risco = gerente.aplica_risco(arquivo=PLANILHA_TEST)
        # print(lista_risco)
        # assert False


if __name__ == '__main__':
    # Cria no banco atualmente configurado os objetos de teste
    # Apenas para praticidade durante o período inicial de testes
    mysession = MySession(Base, test=False)
    dbsession = mysession.session
    print('Atenção, entrando em Base REAL!!!!')
    # gerente = GerenteRisco()
    # gerente.import_named_csv(CSV_NAMEDRISCO_TEST, session=mysession.session)
    # gerente.cria_base('PLANILHA_COV', session=mysession.session)