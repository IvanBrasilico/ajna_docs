"""Módulo responsável pelas funções que aplicam os filtros/parâmetros
de risco cadastrados nos dados. Utiliza pandas para realizar filtragem
"""
import csv
import os
from collections import defaultdict

import pandas as pd

from sentinela.models.models import Filtro, ParametroRisco, ValorParametro


def equality(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    df = df[df[nomecampo].isin(listavalores)]
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

    def add_risco(self, parametrorisco):
        """Configura os parametros de risco ativos"""
        dict_filtros = defaultdict(list)
        for valor in parametrorisco.valores:
            dict_filtros[valor.tipo_filtro].append(valor.valor)
        self.riscosativos[parametrorisco.nome_campo] = dict_filtros

    def remove_risco(self, parametrorisco):
        """Configura os parametros de risco ativos"""
        self.riscosativos.pop(parametrorisco.nome_campo, None)

    def clear_risco(self):
        """Zera os parametros de risco ativos"""
        self.riscosativos = {}

    def aplica_risco(self, lista=None, arquivo=None):
        """Compara a linha de título da lista recebida com a lista de nomes
        de campo que possuem parâmetros de risco ativos. Após, chama para cada
         campo encontrado a função de filtragem
        lista: Lista a ser filtrada, primeira linha deve conter os nomes dos
            campos idênticos aos definidos no nome_campo do parâmetro de risco
            cadastrado.
        arquivo: Arquivo csv contendo a lista a ser filtrada
        """
        mensagem = "Arquivo não fornecido!"
        if arquivo:
            mensagem = "Lista não fornecida!"
            with open(arquivo, 'r', encoding='iso-8859-1') as arq:
                reader = csv.reader(arq)
                lista = [linha for linha in reader]

        if not lista:
            raise AttributeError("Erro! " + mensagem)

        for r in range(len(lista)):
            lista[r] = list(map(str.strip, lista[r]))
        headers = set(lista[0])
        riscos = set(list(self.riscosativos.keys()))
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

    def parametros_tocsv(self, dest_path='/tmp'):
        """Salva os parâmetros adicionados a um gerente em um arquivo csv
        Ver também: parametros_fromcsv"""
        for campo, dict_filtros in self.riscosativos.items():
            lista = []
            lista.append(('valor', 'tipo_filtro'))
            for tipo_filtro, lista_filtros in dict_filtros.items():
                for valor in lista_filtros:
                    lista.append((valor, tipo_filtro.name))
            with open(os.path.join(dest_path, campo + '.csv'), 'w') as f:
                writer = csv.writer(f)
                writer.writerows(lista)

    def parametros_fromcsv(self, campo, session=None, lista=None, dest_path='/tmp'):
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
            with open(os.path.join(dest_path, campo + '.csv'), 'r') as f:
                reader = csv.reader(f)
                lista = [linha for linha in reader]
                lista = lista[1:]
        if session:
            parametro = session.query(
                ParametroRisco).filter(ParametroRisco.nome == campo).first()
            if not parametro:
                parametro = ParametroRisco(campo)
                session.add(parametro)
            for linha in lista:
                if parametro.id:
                    valor = session.query(ValorParametro).filter(
                        ValorParametro.valor == linha[0],
                        ValorParametro.risco_id == parametro.id).first()
                    valor.tipo_filtro = Filtro[linha[1]]
                    session.merge(valor)
                    if not valor:
                        valor = ValorParametro(linha[0].strip(),
                                               linha[1].strip())
                        session.add(valor)
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
        arquivo: Nome e caminho do arquivo .csv
        session: sessão ativa com BD
        filtro: Tipo de filtro a ser assumido como padrão"""
        with open(arquivo, 'r') as f:
            reader = csv.reader(f)
            cabecalho = next(reader)
            listas = defaultdict(list)
            for linha in reader:
                ind = 0
                for coluna in linha:
                    listas[cabecalho[ind].strip()].append(
                        [coluna.strip(), filtro.name])
                    ind += 1
        for key, value in listas.items():
            self.parametros_fromcsv(key, session, value)
