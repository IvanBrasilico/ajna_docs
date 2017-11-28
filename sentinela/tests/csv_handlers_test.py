import csv
import io
import os
import tempfile
import unittest
from zipfile import ZipFile

from sentinela.utils.csv_handlers import (ascii_sanitizar, muda_titulos_csv,
                                          muda_titulos_lista, sanitizar,
                                          sch_processing, unicode_sanitizar,
                                          ENCODE)

tmpdir = tempfile.mkdtemp()

CSV_TITLES_TEST = 'sentinela/tests/csv_title_example.csv'
SCH_FILE_TEST = 'sentinela/tests/'
SCH_ZIP_TEST = 'sentinela/tests/tests.zip'


class TestCsvHandlers(unittest.TestCase):
    titulos_novos = {'titulo1_old': 'titulo1_new',
                     'titulo2_old': 'titulo2_new'}

    def setUp(self):
        with open(CSV_TITLES_TEST, 'r', encoding=ENCODE, newline='') as f:
            reader = csv.reader(f)
            self.lista = [linha for linha in reader]
        self.tmpdir = tempfile.mkdtemp()
        # Ensure the file is read/write by the creator only
        self.saved_umask = os.umask(0o077)

    def tearDown(self):
        os.umask(self.saved_umask)
        os.rmdir(self.tmpdir)

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
        with open(filenames[0][1], 'r', encoding=ENCODE, newline='') as txt_file:
            reader=csv.reader(txt_file, delimiter='\t')
            lista = [linha for linha in reader]
        with open(filenames[0][0], 'r', encoding=ENCODE, newline='') as csv_file:
            reader = csv.reader(csv_file)
            lista2 = [linha for linha in reader]
        assert len(lista) == len(lista2)
        print(lista[0])
        assert lista[1][0][0:5] == lista2[1][0][0:5]

    def test_sch_zip(self):
        filenames = sch_processing(SCH_ZIP_TEST)
        with ZipFile(SCH_ZIP_TEST) as myzip:
            with myzip.open(filenames[0][1]) as zip_file:
                zip_io = io.TextIOWrapper(
                    zip_file,
                    encoding=ENCODE, newline=None
                )
                reader=csv.reader(zip_io, delimiter='\t')
                lista = [linha for linha in reader]
        print(filenames[0][1])
        print(filenames[0][0])
        with open(filenames[0][0], 'r', encoding=ENCODE, newline='') as txt_file:
            reader = csv.reader(txt_file)
            lista2 = [linha for linha in reader]
        assert len(lista) == len(lista2)
        print('test_sch lista', lista[:2])
        print('test_sch lista2', lista2[:2])
        assert lista[1][0:5] == lista2[1][0:5]

    def test_sanitizar(self):
        for norm_function in {ascii_sanitizar,
                              unicode_sanitizar}:
            teste = 'teste'
            esperado = 'teste'
            sanitizado = sanitizar(teste, norm_function=norm_function)
            assert sanitizado == esperado
            teste = 'Cafézinho'
            esperado = 'cafezinho'
            sanitizado = sanitizar(teste, norm_function=norm_function)
            assert teste != sanitizado
            assert sanitizado == esperado
            teste = 'LOUCO     dos  espAçõs e   Tabulações!!!'
            esperado = 'louco dos espacos e tabulacoes!!!'
            sanitizado = sanitizar(teste, norm_function=norm_function)
            assert teste != sanitizado
            assert sanitizado == esperado
            teste = 'Cafézinho não pode estar frio!!! 2017-11-28. ' + \
                'teste Sentença comprida, Ruian  Metals ou ruian metals?'
            esperado = 'cafezinho nao pode estar frio!!! 2017-11-28. ' + \
                'teste sentenca comprida, ruian metals ou ruian metals?'
            sanitizado = sanitizar(teste, norm_function=norm_function)
            assert teste != sanitizado
            assert sanitizado == esperado
