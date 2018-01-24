"""Testa gerente_base, um navegador simples de bases de dados
Caso chamado diretamente, cria uma base carga de testes
Testes estão sendo feitos na base padrão carga, mas gerente_base
deve funcionar com qualquer base que implemente o mesmo padrão que
a base carga.
"""
import unittest

from sentinela.models.carga import (AtracDesatracEscala, Base, ContainerVazio,
                                    Escala, EscalaManifesto, Manifesto,
                                    MySession)
from sentinela.utils.gerente_base import Filtro, GerenteBase

CSV_FOLDER_TEST = 'sentinela/tests/CSV'


class TestModel(unittest.TestCase):
    def setUp(self):
        self.gerente = GerenteBase()
        mysession = MySession(Base, test=False, nomebase='cargatest.db')
        self.dbsession = mysession.session
        self.engine = mysession.engine

    def tearDown(self):
        pass

    def _escala(self, dict_models):
        assert dict_models is not None
        escala = dict_models['Escala']
        assert escala is not None
        assert 'Escala' in escala['campos']

    def test_lista_model(self):
        self.gerente.set_module('carga')
        assert 'Conhecimento' in self.gerente.list_models
        self._escala(self.gerente.dict_models)

    def test_lista_dir(self):
        # TODO: criar arquivo de testes
        self.gerente.set_path('1/2017/0329', test=True)
        self._escala(self.gerente.dict_models)

    def test_filtra(self):
        self.gerente.set_module('carga')
        afilter = Filtro('Container', None, 'C-C02')
        assert afilter is not None
        self.gerente.set_session(self.dbsession)
        dados = self.gerente.filtra(
            'ContainerVazio', [afilter])
        assert dados is not None

    def test_tree(self):
        escala = self.dbsession.query(Escala).filter(
            Escala.Escala == 'E-1').first()
        if escala:
            lista = self.gerente.recursive_tree(escala)
            print(lista)
            with open('tree.html', 'w') as html:
                for linha in lista:
                    html.write('{}\n'.format(linha))
        assert '<ul' in lista[0]

    def test_buscapai(self):
        escala = self.dbsession.query(Escala).filter(
            Escala.Escala == 'E-1').first()
        if escala:
            instance = self.gerente.busca_paiarvore(escala)
            print(instance)
        assert instance is not None


if __name__ == '__main__':
    unittest.main()
