import unittest
from datetime import date

from sentinela.models.models import (Base, Filtro, MySession, ParametroRisco,
                                     ValorParametro)


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_risco(self):
        risco = ParametroRisco('teste', 'teste')
        assert risco.nome == 'teste'
        assert risco.descricao == 'teste'
        self.session.add(risco)
        self.session.commit()
        assert risco.id is not None

    def test_valor(self):
        risco = ParametroRisco('teste', 'teste')
        valor = ValorParametro('teste', Filtro.startswith)
        assert valor.nome_campo == 'teste'
        assert valor.tipo_filtro is Filtro.startswith
        self.session.add(valor)
        self.session.commit()
        risco.valores.append(valor)
        self.session.add(risco)
        self.session.commit()
        assert len(risco.valores) == 1
        assert risco.valores[0].nome_campo == 'teste'
