import unittest

from sentinela.utils.gerente_base import GerenteBase


class TestModel(unittest.TestCase):
    def setUp(self):
        self.gerente = GerenteBase()

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
