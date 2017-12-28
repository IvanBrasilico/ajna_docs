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
        # self.gerente.set_path('1/2017/1221')
        # self._escala(self.gerente.dict_models)
        pass

    def test_filtra(self):
        self.gerente.set_module('carga')
        afilter = Filtro('CPFCNPJNotificado', None, '000000')
        assert afilter is not None
        # TODO: criar base carga de testes
        self.gerente.set_session(self.dbsession)
        """dados = self.gerente.filtra(
            'Conhecimento', [afilter])  # , self.dbsession)
        assert dados is not None"""

    def test_tree(self):
        # TODO: criar base carga de testes
        # pass
        escala = self.dbsession.query(Escala).filter(
            Escala.Escala == 'E-1').first()
        if escala:
            lista = self.gerente.recursive_tree(escala)
            print(lista)
            with open('tree.html', 'w') as html:
                for linha in lista:
                    html.write('{}\n'.format(linha))
        assert '<ul>' in lista[0]


if __name__ == '__main__':
    mysession = MySession(Base, test=False, nomebase='cargatest.db')
    dbsession = mysession.session
    engine = mysession.engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    escala = Escala()
    escala.Escala = 'E-1'
    escala.CNPJAgenciaNavegacao = 'E-C01'
    escala.CodigoIMO = 'E-IMO01'
    dbsession.add(escala)
    atracacao = AtracDesatracEscala()
    atracacao.Escala = 'E-1'
    atracacao.CodigoTerminal = 'A-T01'
    dbsession.add(atracacao)
    manifesto = Manifesto()
    manifesto.Manifesto = 'M-2'
    dbsession.add(manifesto)
    escalamanifesto = EscalaManifesto()
    escalamanifesto.Escala = 'E-1'
    escalamanifesto.Manifesto = 'M-2'
    dbsession.add(escalamanifesto)
    vazio = ContainerVazio()
    vazio.Manifesto = 'M-2'
    vazio.Container = 'C-C01'
    vazio.Capacidade = 'C-40'
    dbsession.add(vazio)
    vazio2 = ContainerVazio()
    vazio2.Manifesto = 'M-2'
    vazio2.Container = 'C-C02'
    vazio2.Capacidade = 'C-40'
    dbsession.add(vazio2)
    dbsession.commit()
    unittest.main()
