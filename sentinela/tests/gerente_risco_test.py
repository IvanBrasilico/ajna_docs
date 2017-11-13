import csv
import unittest

from sentinela.utils.gerente_risco import GerenteRisco
from sentinela.models.models import Filtro

CSV_RISCO_TEST = 'sentinela/tests/csv_risco_example.csv'


class TestCsvHandlers(unittest.TestCase):

    def setUp(self):
        with open(CSV_RISCO_TEST, 'r') as f:
            reader = csv.reader(f)
            self.lista = [linha for linha in reader]
        self.gerente = GerenteRisco()

    def tearDown(self):
        pass

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
