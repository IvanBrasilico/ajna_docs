"""Testes para o módulo gerente_risco"""
import csv
import os
import tempfile
import unittest

from sentinela.models.models import Filtro
from sentinela.utils.gerente_risco import GerenteRisco

CSV_RISCO_TEST = 'sentinela/tests/csv_risco_example.csv'
CSV_NAMEDRISCO_TEST = 'sentinela/tests/csv_namedrisco_example.csv'


class TestGerenteRisco(unittest.TestCase):

    def setUp(self):
        with open(CSV_RISCO_TEST, 'r') as f:
            reader = csv.reader(f)
            self.lista = [linha for linha in reader]
        self.gerente = GerenteRisco()
        self.tmpdir = tempfile.mkdtemp()
        # Ensure the file is read/write by the creator only
        self.saved_umask = os.umask(0o077)

    def tearDown(self):
        os.umask(self.saved_umask)

    def test_aplica_igual(self):
        lista = self.lista
        gerente = self.gerente
        bacon = type('ValorParametro', (object, ),
                     {'tipo_filtro': Filtro.igual,
                      'valor': 'bacon'
                      })
        coxinha = type('ValorParametro', (object, ),
                       {'tipo_filtro': Filtro.igual,
                        'valor': 'coxinha'
                        })
        basejump = type('ValorParametro', (object, ),
                        {'tipo_filtro': Filtro.igual,
                         'valor': 'basejump'
                         })
        surf = type('ValorParametro', (object, ),
                    {'tipo_filtro': Filtro.igual,
                     'valor': 'surf'
                     })
        madrugada = type('ValorParametro', (object, ),
                         {'tipo_filtro': Filtro.igual,
                          'valor': 'madrugada'
                          })
        alimentos = type('ParametroRisco', (object, ),
                         {'nome_campo': 'alimento',
                          'valores': [bacon, coxinha]}
                         )
        esportes = type('ParametroRisco', (object, ),
                        {'nome_campo': 'esporte',
                         'valores': [surf, basejump]}
                        )
        horarios = type('ParametroRisco', (object, ),
                        {'nome_campo': 'horario',
                         'valores': [madrugada]}
                        )

        gerente.add_risco(alimentos)
        gerente.add_risco(esportes)
        gerente.add_risco(horarios)
        lista_risco = gerente.aplica_risco(lista)
        print(lista_risco)
        assert len(lista_risco) == 5
        gerente.remove_risco(horarios)
        lista_risco = gerente.aplica_risco(lista)
        print(lista_risco)
        assert len(lista_risco) == 4
        gerente.remove_risco(esportes)
        lista_risco = gerente.aplica_risco(lista)
        print(lista_risco)
        assert len(lista_risco) == 2

    def test_aplica_comeca_com(self):
        lista = self.lista
        gerente = self.gerente
        bacon = type('ValorParametro', (object, ),
                     {'tipo_filtro': Filtro.comeca_com,
                      'valor': 'baco'
                      })
        coxinha = type('ValorParametro', (object, ),
                       {'tipo_filtro': Filtro.comeca_com,
                        'valor': 'cox'
                        })
        basejump = type('ValorParametro', (object, ),
                        {'tipo_filtro': Filtro.comeca_com,
                         'valor': 'base'
                         })
        surf = type('ValorParametro', (object, ),
                    {'tipo_filtro': Filtro.comeca_com,
                     'valor': 'sur'
                     })
        alimentos = type('ParametroRisco', (object, ),
                         {'nome_campo': 'alimento',
                          'valores': [bacon, coxinha]}
                         )
        esportes = type('ParametroRisco', (object, ),
                        {'nome_campo': 'esporte',
                         'valores': [surf, basejump]}
                        )
        gerente.add_risco(alimentos)
        gerente.add_risco(esportes)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 4
        gerente.remove_risco(esportes)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 2

    def test_aplica_contem(self):
        lista = self.lista
        gerente = self.gerente
        bacon = type('ValorParametro', (object, ),
                     {'tipo_filtro': Filtro.contem,
                      'valor': 'aco'
                      })
        coxinha = type('ValorParametro', (object, ),
                       {'tipo_filtro': Filtro.contem,
                        'valor': 'xinh'
                        })
        basejump = type('ValorParametro', (object, ),
                        {'tipo_filtro': Filtro.contem,
                         'valor': 'jump'
                         })
        surf = type('ValorParametro', (object, ),
                    {'tipo_filtro': Filtro.contem,
                     'valor': 'urf'
                     })
        alimentos = type('ParametroRisco', (object, ),
                         {'nome_campo': 'alimento',
                          'valores': [bacon, coxinha]}
                         )
        esportes = type('ParametroRisco', (object, ),
                        {'nome_campo': 'esporte',
                         'valores': [surf, basejump]}
                        )
        gerente.add_risco(alimentos)
        gerente.add_risco(esportes)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 4
        gerente.remove_risco(esportes)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 2

    def test_aplica_namedcsv(self):
        lista = self.lista
        gerente = self.gerente
        gerente.import_named_csv(CSV_NAMEDRISCO_TEST)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 5

    def test_parametrostocsv(self):
        lista = self.lista
        gerente = self.gerente
        gerente.import_named_csv(CSV_NAMEDRISCO_TEST)
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 5
        gerente.parametros_tocsv()
        gerente.clear_risco()
        gerente.parametros_fromcsv('alimento')
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 2
        gerente.clear_risco()
        gerente.parametros_fromcsv('esporte')
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 2
        gerente.clear_risco()
        gerente.parametros_fromcsv('horario')
        lista_risco = gerente.aplica_risco(lista)
        assert len(lista_risco) == 1

    def test_juntacsv(self):
        gerente = self.gerente
        autores = type('Tabela', (object, ),
                       {'csv': 'autores.csv',
                        'estrangeiro': 'livroid'
                        })
        sub_capitulos = type('Tabela', (object, ),
                             {'csv': 'subcapitulos.csv',
                              'estrangeiro': 'capituloid',
                              'type': 'outer'
                              })
        capitulos = type('Tabela', (object, ),
                         {'csv': 'capitulos.csv',
                          'primario': 'id',
                          'estrangeiro': 'livroid',
                          'filhos': [sub_capitulos]
                          })
        autores_livro = type('Tabela', (object, ),
                             {'nome': 'autores_livro',
                              'csv': 'livros.csv',
                              'primario': 'id',
                              'filhos': [autores]
                              })
        capitulos_livro = type('Tabela', (object, ),
                               {'nome': 'capitulos_livro',
                                'csv': 'livros.csv',
                                'primario': 'id',
                                'filhos': [capitulos]
                                })
        path = 'sentinela/tests/juncoes'
        result = gerente.aplica_juncao(autores_livro, path=path)
        print(result)
        assert len(result) == 3
        print(list(result['livroid'].items()))
        assert list(result['livroid'].items()) == [(0, 1), (1, 1), (2, 2)]
        # TODO: Melhorar verificações (asserts) desta parte
        result = gerente.aplica_juncao(capitulos_livro, path=path)
        assert len(result) == 8
        assert list(result['livroid'].items()) == [(0, 1),
                                                   (1, 1),
                                                   (2, 1),
                                                   (3, 1),
                                                   (4, 1),
                                                   (5, 1),
                                                   (6, 2),
                                                   (7, 2)]
        print(result)
        # assert False  # Uncomment to view output
