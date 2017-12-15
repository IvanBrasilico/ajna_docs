"""Exemplo de utilização no sistema CARGA.
Teste funcional simulando utilização com uma base "real".
A base é uma base do Sistema Siscomex Carga modificada por questões de sigilo.
"""
import os
import tempfile
import unittest

from sentinela.models.models import (Base, BaseOriginal, Filtro, MySession,
                                     ParametroRisco, ValorParametro)
from sentinela.utils.csv_handlers import sch_processing
from sentinela.utils.gerente_risco import GerenteRisco

# Configurar nesta linha uma base do Sistema Carga E
CARGA_ZIP_TEST = '/home/ivan/Downloads/P.zip'
# Comentar a linha abaixo para testar com uma base real
CARGA_ZIP_TEST = 'sentinela/tests/tests.zip'


def carrega_carga(session):
    padraorisco = BaseOriginal('CARGA')
    session.add(padraorisco)
    session.commit()
    risco = ParametroRisco('CPFCNPJConsignatario', 'CNPJ do Consignatario', padraorisco=padraorisco)
    session.add(risco)
    # Adicionar um CNPJ que exista na extração, para testar...
    valor = ValorParametro('42581413000157', Filtro.igual)
    session.add(valor)
    risco.valores.append(valor)
    session.merge(risco)
    session.commit()

    risco2 = ParametroRisco('DescricaoMercadoria', 'Descrição', padraorisco=padraorisco)
    session.add(risco2)
    # Adicionar uma mercadoria que exista na extração, para testar...
    valor2 = ValorParametro('PILLOW', Filtro.contem)
    session.add(valor2)
    session.commit()
    risco2.valores.append(valor2)
    session.merge(risco2)
    session.commit()
    session.merge(padraorisco)
    session.commit()
    return padraorisco


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)
        self.tmpdir = tempfile.mkdtemp()
        # Ensure the file is read/write by the creator only
        self.saved_umask = os.umask(0o077)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        os.umask(self.saved_umask)

    def test_carga(self):
        # Define parâmetros de risco. Na interface de usuário estes
        # valores deverão estar persistidos em Banco de Dados e/ou serem
        # exportados ou importados via arquivo .csv
        # (GerenteRisco parametros_tocsv e parametros_fromcsv)
        #########################################################
        # Este precisa de uma extração disponível e é pesado
        # Para não rodar, renomeie o método para no_test_carga
        # O pytest só chama os métodos começados com test
        #
        ###################
        filenames = sch_processing(CARGA_ZIP_TEST)
        print(filenames)
        assert filenames is not None
        # assert(len(filenames) == 14)
        padraorisco = carrega_carga(self.session)
        gerente = GerenteRisco()
        gerente.set_base(padraorisco)
        print(padraorisco.parametros[0].valores)
        # Preferencialmente vai tentar processar o arquivo de conhecimentos
        # Se não houver, pega o primeiro da lista mesmo
        ind = 0
        for index, filename in enumerate(filenames):
            if filename[0].find('Conhecimento'):
                ind = index
                break
        with open(filenames[ind][0]) as show_the_head:
            head = [next(show_the_head) for x in range(5)]
        print(head)
        result = gerente.aplica_risco(arquivo=filenames[ind][0])
        print(result)
        # assert False  # To view output, uncomment this

        # TODO:  Testar gerente.aplica_juncao() em uma base do Carga


if __name__ == '__main__':
    # Cria no banco atualmente configurado os objetos da função carrega_carga
    # Apenas para praticidade durante o período inicial de testes
    mysession = MySession(Base, test=False)
    carrega_carga(mysession.session)
