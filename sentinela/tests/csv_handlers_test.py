import unittest

from sentinela.csv_handlers import (muda_titulos_csv,
                                    muda_titulos_lista)

CSV_TITLES_TEST = 'sentinela/tests/csv_title_example.csv'


class TestCsvHandlers(unittest.TestCase):
    titulos_novos = {'titulo1_old': 'titulo1_new',
                     'titulo2_old': 'titulo2_new'}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_muda_titulos_csv(self):
        with open(CSV_TITLES_TEST) as csv:
            lista_old = csv.readlines()
        lista = muda_titulos_csv(CSV_TITLES_TEST,
                                 TestCsvHandlers.titulos_novos)
        self.comparalistas(lista_old, lista)

    def test_muda_titulos_lista(self):
        with open(CSV_TITLES_TEST) as csv:
            lista = csv.readlines()
        lista_old = list(lista)
        muda_titulos_lista(lista, TestCsvHandlers.titulos_novos)
        self.comparalistas(lista_old, lista)

    def comparalistas(self, lista_old, lista):
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert old in lista_old[0]
            assert new not in lista_old[0]
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert new in lista[0]
