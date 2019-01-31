import unittest

from ajna_commons.utils.sanitiza import (ascii_sanitizar, mongo_sanitizar,
                                         sanitizar,
                                         sanitizar_lista, unicode_sanitizar)


class TestModel(unittest.TestCase):

    def test_sanitizar(self):
        antes = 'TESTE de SANitização   bagunçado.'
        antes2 = 'Teste número 2'
        depois = 'teste de sanitizacao baguncado.'
        depois2 = 'teste numero 2'
        s = sanitizar(antes)
        assert s == depois
        s = sanitizar(antes, norm_function=ascii_sanitizar)
        assert s == depois
        s = sanitizar(antes, norm_function=unicode_sanitizar)
        assert s == depois
        lista = [antes, antes2]
        listas = sanitizar_lista(lista)
        assert listas[0] == depois
        assert listas[1] == depois2
        lista = [[antes, antes2], [antes2, antes]]
        listas = sanitizar_lista(lista)
        assert listas[0][0] == depois
        assert listas[0][1] == depois2
        assert listas[1][1] == depois
        assert listas[1][0] == depois2

    def test_mongo_sanitizar(self):
        teste = '{$where: \'atacking\': "DANGEROUS! Test. 2.53"}function();}'
        esperado = 'where atacking DANGEROUS! Test. 2.53function'
        resultado = mongo_sanitizar(teste)
        print(resultado)
        assert resultado == esperado


if __name__ == '__main__':
    unittest.main()
