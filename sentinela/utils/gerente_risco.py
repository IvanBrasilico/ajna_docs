"""Módulo responsável pelas funções que aplicam os filtros/parâmetros
de risco cadastrados nos dados. Utiliza pandas para realizar filtragem
"""
import csv
import os
import tempfile
from collections import defaultdict

import pandas as pd

from sentinela.models.models import (BaseOriginal, Filtro, ParametroRisco,
                                     ValorParametro)

tmpdir = tempfile.mkdtemp()


def equality(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    df = df[df[nomecampo].isin(listavalores)]
    print(df[nomecampo][:9])
    return df.values.tolist()


def startswith(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    result = []
    for valor in listavalores:
        df = df[df[nomecampo].str.startswith(valor, na=False)]
        result.append(df.values.tolist())
    return result


def contains(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    result = []
    for valor in listavalores:
        df = df[df[nomecampo].str.contains(valor, na=False)]
        result.append(df.values.tolist())
    return result


filter_functions = {
    Filtro.igual: equality,
    Filtro.comeca_com: startswith,
    Filtro.contem: contains
}


class GerenteRisco():

    def __init__(self):
        self.riscosativos = {}
        self.riscos = []
        self.base = None

    def set_base(self, base, session=None):
        """Vincula o Gerente a um objeto BaseOriginal
        Atenção: TODOS os parâmetros de risco ativos no Gerente serão
        adicionados a esta base!!!
        TODOS os parâmetros de risco vinculados à BaseOriginal serão
        adicionados aos riscos ativos!!!
        """
        self.base = base
        if session and self.riscos:
            for risco in self.riscos:
                self.base.parametros.append(risco)
            session.merge(base)
            session.commit()
        self.riscos = self.base.parametros

    def cria_base(self, nomebase, session):
        base = session.query(BaseOriginal).filter(
            BaseOriginal.nome == nomebase).first()
        if not base:
            base = BaseOriginal(nomebase)
        self.set_base(base, session)

    def add_risco(self, parametrorisco, session=None):
        """Configura os parametros de risco ativos"""
        dict_filtros = defaultdict(list)
        for valor in parametrorisco.valores:
            dict_filtros[valor.tipo_filtro].append(valor.valor)
        self.riscosativos[parametrorisco.nome_campo] = dict_filtros
        self.riscos.append(parametrorisco)
        if session and self.base:
            self.base.parametros.append(parametrorisco)
            session.merge(self.base)
            session.commit()

    def remove_risco(self, parametrorisco, session=None):
        """Configura os parametros de risco ativos"""
        self.riscosativos.pop(parametrorisco.nome_campo, None)
        self.riscos.remove(parametrorisco)
        if session and self.base:
            self.base.parametros.remove(parametrorisco)
            session.merge(self.base)
            session.commit()

    def clear_risco(self, session=None):
        """Zera os parametros de risco ativos"""
        self.riscosativos = {}
        self.riscos.clear()
        if session and self.base:
            self.base.parametros.clear()
            session.merge(self.base)
            session.commit()

    def aplica_risco(self, lista=None, arquivo=None):
        """Compara a linha de título da lista recebida com a lista de nomes
        de campo que possuem parâmetros de risco ativos. Após, chama para cada
        campo encontrado a função de filtragem
        lista: Lista a ser filtrada, primeira linha deve conter os nomes dos
            campos idênticos aos definidos no nome_campo do parâmetro de risco
            cadastrado.
        arquivo: Arquivo csv contendo a lista a ser filtrada
        """
        mensagem = 'Arquivo não fornecido!'
        if arquivo:
            mensagem = 'Lista não fornecida!'
            with open(arquivo, 'r', encoding='iso-8859-1', newline='') as arq:
                reader = csv.reader(arq)
                lista = [linha for linha in reader]

        if not lista:
            raise AttributeError('Erro! ' + mensagem)

        for r in range(len(lista)):
            lista[r] = list(map(str.strip, lista[r]))
        headers = set(lista[0])
        print('Headers:', headers)
        riscos = set(list(self.riscosativos.keys()))
        print('Riscos:', riscos)
        aplicar = headers & riscos   # UNION OF SETS
        print('Aplicar:', aplicar)
        result = []
        for campo in aplicar:
            dict_filtros = self.riscosativos.get(campo)
            for tipo_filtro, lista_filtros in dict_filtros.items():
                filter_function = filter_functions.get(tipo_filtro)
                if filter_function is None:
                    raise NotImplementedError('Função de filtro' +
                                              tipo_filtro.name +
                                              ' não implementada.')
                result_campo = filter_function(lista, campo, lista_filtros)
                for linha in result_campo:
                    result.append(linha)
        print(result)
        return result

    def parametros_tocsv(self, path=tmpdir):
        """Salva os parâmetros adicionados a um gerente em um arquivo csv
        Ver também: parametros_fromcsv"""
        for campo, dict_filtros in self.riscosativos.items():
            lista = []
            lista.append(('valor', 'tipo_filtro'))
            for tipo_filtro, lista_filtros in dict_filtros.items():
                for valor in lista_filtros:
                    lista.append((valor, tipo_filtro.name))
            with open(os.path.join(path, campo + '.csv'),
                      'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(lista)

    def parametros_fromcsv(self, campo, session=None,
                           lista=None, path=tmpdir):
        """Abre um arquivo csv, recupera parâmetros configurados nele,
        adiciona à configuração do gerente e **também adiciona ao Banco de
        Dados ativo** caso não existam nele ainda. Para isso é preciso
        passar a session como parâmetro, senão cria apenas na memória
        Pode receber uma lista no lugar de um arquivo csv (como implementado
        em import_named_csv)
        Ver também: parametros_tocsv, import_named_csv
        campo: nome do campo a ser filtrado e deve ser também
            o nome do arquivo .csv
        session: a sessão com o banco de dados
        lista: passar uma lista pré-prenchida para usar a função com outros
            tipos de fontes/arquivos. Se passada uma lista, função não
            abrirá arquivo .csv, usará os valores da função

        O arquivo .csv ou a lista DEVEM estar no formato valor, tipo_filtro
        """
        if not lista:
            with open(os.path.join(path, campo + '.csv'),
                      'r', newline='') as f:
                reader = csv.reader(f)
                lista = [linha for linha in reader]
                lista = lista[1:]
        if session:
            parametro = session.query(ParametroRisco).filter(
                ParametroRisco.nome_campo == campo).first()
            if not parametro:
                parametro = ParametroRisco(campo)
                session.add(parametro)
                session.commit()
            for linha in lista:
                if parametro.id:
                    valor = session.query(ValorParametro).filter(
                        ValorParametro.valor == linha[0],
                        ValorParametro.risco_id == parametro.id).first()
                    if not valor:
                        valor = ValorParametro(linha[0].strip(),
                                               linha[1].strip())
                        session.add(valor)
                    else:
                        valor.tipo_filtro = Filtro[linha[1]]
                        session.merge(valor)
                    parametro.valores.append(valor)
            session.merge(parametro)
            session.commit()
            self.add_risco(parametro)
        else:
            dict_filtros = defaultdict(list)
            for linha in lista:
                dict_filtros[Filtro[linha[1]]].append(linha[0])
            self.riscosativos[campo] = dict_filtros

    def import_named_csv(self, arquivo, session=None, filtro=Filtro.igual):
        """Abre um arquivo csv, cada coluna sendo um filtro.
        A primeira linha contém o campo a ser filtrado e as linhas
        seguintes os valores do filtro. Cria filtros na memória, e no
        Banco de Dados caso session seja informada.

        @params

            arquivo: Nome e caminho do arquivo .csv
            session: sessão ativa com BD
            filtro: Tipo de filtro a ser assumido como padrão

        """
        with open(arquivo, 'r', newline='') as f:
            reader = csv.reader(f)
            cabecalho = next(reader)
            listas = defaultdict(list)
            for linha in reader:
                ind = 0
                for coluna in linha:
                    coluna = coluna.strip()
                    if coluna:
                        listas[cabecalho[ind].strip()].append(
                            [coluna, filtro.name])
                    ind += 1
        for key, value in listas.items():
            self.parametros_fromcsv(key, session, value)

    def recurse_merge(self, tabela):
        if tabela.filhos:
            if len(tabela.filhos) == 1:
                return tabela.filhos[0]

    def aplica_juncao(self, tabela, path=tmpdir, arvore=False):
        paifilename = os.path.join(path, tabela.csv)
        dfpai = pd.read_csv(paifilename)
        for filho in tabela.filhos:
            if hasattr(filho, 'filhos') and filho.filhos:
                dffilho = self.aplica_juncao(filho, path, arvore)
            else:
                filhofilename = os.path.join(path, filho.csv)
                dffilho = pd.read_csv(filhofilename)
            if hasattr(filho, 'type'):
                how = filho.type
            else:
                how = 'inner'
            result = dfpai.merge(dffilho, how=how,
                                 left_on=tabela.primario,
                                 right_on=filho.estrangeiro)
        return result
