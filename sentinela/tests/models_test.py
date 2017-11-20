import unittest
from datetime import date

from sentinela.models.models import (Base, BaseOriginal, Filtro, MySession,
                                     ParametroRisco, ValorParametro)


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test1_risco(self):
        risco = ParametroRisco('teste', 'teste')
        assert risco.nome_campo == 'teste'
        assert risco.descricao == 'teste'
        self.session.add(risco)
        self.session.commit()
        assert risco.id is not None

    def test2_valor(self):
        risco = ParametroRisco('teste1', 'teste2')
        assert risco.nome_campo == 'teste1'
        valor = ValorParametro('teste3', Filtro.igual)
        assert valor.valor == 'teste3'
        assert valor.tipo_filtro is Filtro.igual
        self.session.add(valor)
        self.session.commit()
        risco.valores.append(valor)
        self.session.add(risco)
        self.session.commit()
        assert len(risco.valores) == 1
        valor = risco.valores[0]
        assert valor.valor == 'teste3'
        assert valor.risco.nome_campo == 'teste1'
        assert valor.risco.descricao == 'teste2'

    def test_base_original(self):
        base = BaseOriginal('nome', 'caminho')
        assert base.nome == 'nome'
        assert base.caminho == 'caminho'
        self.session.add(base)
        self.session.commit()
        risco = ParametroRisco('teste', 'teste')
        self.session.add(risco)
        self.session.commit()
        assert risco.id is not None
        risco = self.session.query(ParametroRisco).filter(
            ParametroRisco.nome_campo == 'teste').first()
        base.parametros.append(risco)
        self.session.merge(base)
        self.session.commit()
        assert len(base.parametros) == 1
        risco = base.parametros[0]
        assert risco.base.nome == 'nome'
        assert risco.base.caminho == 'caminho'
