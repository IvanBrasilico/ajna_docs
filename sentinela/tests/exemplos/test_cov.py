"""Exemplo de utilização no sistema COV.
Teste funcional simulando utilização com uma base "real".
"""
import os
import tempfile
import unittest

from sentinela.models.models import Base, BaseOrigem, DePara, MySession
from sentinela.utils.gerente_risco import GerenteRisco

PLANILHA_TEST = '/home/ivan/Downloads/planilhaBTP.csv'
CSV_NAMEDRISCO_TEST = 'sentinela/tests/csv_namedrisco_example.csv'


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
        depara1 = DePara('antigo1', 'novo1', base)
        self.session.add(depara1)
        depara2 = DePara('antigo2', 'novo2', base)
        self.session.add(depara2)
        self.session.commit()
        de_para_dict = {depara.titulo_ant:depara.titulo_novo for depara in base.deparas}
        print(de_para_dict)
        # lista_old = 
        lista = muda_titulos_lista(lista_old,
                                        de_para_dict)
        for old, new in de_para_dict:
            assert old in ''.join(lista_old[0])
            assert new not in ''.join(lista_old[0])
        for old, new in de_para_dict:
            assert new in ''.join(lista[0])

        assert False


if __name__ == '__main__':
    # Cria no banco atualmente configurado os objetos de teste
    # Apenas para praticidade durante o período inicial de testes
    mysession = MySession(Base, test=False)
    print("Atenção, entrando em Base REAL!!!!")
    # gerente = GerenteRisco()
    # gerente.import_named_csv(CSV_NAMEDRISCO_TEST, session=mysession.session)
    # gerente.cria_base('PLANILHA_COV', session=mysession.session)
