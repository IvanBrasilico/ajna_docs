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
        pass

    def test_muda_titulos_lista(self):
        with open(CSV_TITLES_TEST) as csv:
            lista = csv.readlines()
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert old in lista[0]
            assert new not in lista[0]
        muda_titulos_lista(lista, TestCsvHandlers.titulos_novos)
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert new in lista[0]
