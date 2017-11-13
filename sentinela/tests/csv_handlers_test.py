import csv
import unittest

from sentinela.utils.csv_handlers import (muda_titulos_csv, muda_titulos_lista,
                                          sch_processing)

CSV_TITLES_TEST = 'sentinela/tests/csv_title_example.csv'
SCH_FILE_TEST = 'sentinela/tests/'
SCH_ZIP_TEST = 'sentinela/tests/tests.zip'


class TestCsvHandlers(unittest.TestCase):
    titulos_novos = {'titulo1_old': 'titulo1_new',
                     'titulo2_old': 'titulo2_new'}

    def setUp(self):
        with open(CSV_TITLES_TEST, 'r') as f:
            reader = csv.reader(f)
            self.lista = [linha for linha in reader]

    def tearDown(self):
        pass

    def test_muda_titulos_csv(self):
        lista_nova = muda_titulos_csv(CSV_TITLES_TEST,
                                      TestCsvHandlers.titulos_novos)
        self.comparalistas(self.lista, lista_nova)

    def test_muda_titulos_lista(self):
        lista_old = list(self.lista)
        self.lista = muda_titulos_lista(self.lista,
                                        TestCsvHandlers.titulos_novos)
        self.comparalistas(lista_old, self.lista)

    def comparalistas(self, lista_old, lista):
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert old in ''.join(lista_old[0])
            assert new not in ''.join(lista_old[0])
        for old, new in TestCsvHandlers.titulos_novos.items():
            assert new in ''.join(lista[0])

    def test_sch_dir(self):
        sch_processing(SCH_FILE_TEST)
        assert False




    def test_sch_zip(self):
        sch_processing(SCH_ZIP_TEST)
        assert False
