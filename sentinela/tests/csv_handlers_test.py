import csv
import unittest
from zipfile import ZipFile

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
        filenames = sch_processing(SCH_FILE_TEST)
        with open(filenames[0][1], 'r', encoding='iso-8859-1') as f:
            reader = csv.reader(f)
            lista = [linha for linha in reader]
        with open(filenames[0][0], 'r') as f:
            reader = csv.reader(f)
            lista2 = [linha for linha in reader]
        assert len(lista) == len(lista2) + 1
        print(lista[0])
        assert lista[1][0][0:5] == lista2[0][0][0:5]

    def test_sch_zip(self):
        filenames = sch_processing(SCH_ZIP_TEST)
        with ZipFile(SCH_ZIP_TEST) as myzip:
            with myzip.open(filenames[0][1]) as zip_file:
                lista = zip_file.readlines()
                lista = [linha.decode('iso-8859-1') for linha in lista]
        with open(filenames[0][0], 'r') as f:
            reader = csv.reader(f)
            lista2 = [linha for linha in reader]
        assert len(lista) == len(lista2) + 1
        print(lista)
        assert lista[1][0:5] == lista2[0][0][0:5]
