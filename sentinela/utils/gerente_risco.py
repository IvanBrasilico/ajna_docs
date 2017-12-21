"""Módulo responsável pelas funções que aplicam os filtros/parâmetros
de risco cadastrados nos dados. Utiliza pandas para realizar filtragem
"""
import csv
import os
import tempfile
from collections import defaultdict

import pandas as pd

from sentinela.models.models import (Filtro, PadraoRisco, ParametroRisco,
                                     ValorParametro)

tmpdir = tempfile.mkdtemp()
ENCODE = 'latin1'


def equality(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    df = df[df[nomecampo].isin(listavalores)]
    return df.values.tolist()


def startswith(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    result = []
    for valor in listavalores:
        df_filtered = df[df[nomecampo].str.startswith(valor, na=False)]
        result.extend(df_filtered.values.tolist())
    return result


def contains(listaoriginal, nomecampo, listavalores):
    df = pd.DataFrame(listaoriginal[1:], columns=listaoriginal[0])
    result = []
    for valor in listavalores:
        df_filtered = df[df[nomecampo].str.contains(valor, na=False)]
        result.extend(df_filtered.values.tolist())
    return result


filter_functions = {
    Filtro.igual: equality,
    Filtro.comeca_com: startswith,
    Filtro.contem: contains
}


class GerenteRisco():
    """Classe que aplica parâmetros de risco e/ou junção em listas

    São fornecidos também metodos para facilitar o de/para entre
    o Banco de Dados e arquivos csv de parâmetros, para permitir que
    Usuário importe e exporte parâmetros de risco.

    Args:
        pre_processers: dict de funções para pré-processar lista. Função
        DEVE esperar uma lista como primeiro parâmetro

        pre_processers_params: se houver, será passado para função com mesmo
        'key' do pre_processer como kargs.

        Ex:

        gerente.pre_processers['mudatitulo'] = muda_titulos

        gerente.pre_processers_params['mudatitulo'] = {'de_para_dict': {}}

        Os atributos abaixo NÂO devem ser acessados diretamente. A classe
        os gerencia internamente.

        riscosativos: dict descreve "riscos" (compilado dos ParametrosRisco)

        base: BaseOriginal ativa
    """

    def __init__(self):
        self.pre_processers = {}
        self.pre_processers_params = {}
        self._riscosativos = {}
        self._base = None

    def set_base(self, base):
        """Vincula o Gerente a um objeto BaseOriginal
        Atenção: TODOS os parâmetros de risco ativos no Gerente serão
        zerados!!!
        TODOS os parâmetros de risco vinculados à BaseOriginal serão
        adicionados aos riscos ativos!!!
        """
        self._base = base
        self._riscosativos = {}
        for parametro in self._base.parametros:
            self.add_risco(parametro)

    def cria_base(self, nomebase, session):
        base = session.query(PadraoRisco).filter(
            PadraoRisco.nome == nomebase).first()
        if not base:
            base = PadraoRisco(nomebase)
        self.set_base(base)

    def add_risco(self, parametrorisco, session=None):
        """Configura os parametros de risco ativos"""
        dict_filtros = defaultdict(list)
        for valor in parametrorisco.valores:
            dict_filtros[valor.tipo_filtro].append(valor.valor)
        self._riscosativos[parametrorisco.nome_campo] = dict_filtros
        if session and self._base:
            self._base.parametros.append(parametrorisco)
            session.merge(self._base)
            session.commit()

    def remove_risco(self, parametrorisco, session=None):
        """Configura os parametros de risco ativos"""
        self._riscosativos.pop(parametrorisco.nome_campo, None)
        if session and self._base:
            self._base.parametros.remove(parametrorisco)
            session.merge(self._base)
            session.commit()

    def clear_risco(self, session=None):
        """Zera os parametros de risco ativos"""
        self._riscosativos = {}
        if session and self._base:
            self._base.parametros.clear()
            session.merge(self._base)
            session.commit()

    def aplica_risco(self, lista=None, arquivo=None, parametros_ativos=None):
        """Compara a linha de título da lista recebida com a lista de nomes
        de campo que possuem parâmetros de risco ativos. Após, chama para cada
        campo encontrado a função de filtragem. Somente um dos parâmetros
        precisa ser passado. Caso na lista do pipeline estejam cadastradas
        funções de pré-processamento, serão aplicadas.

        Args:
            lista (list): Lista a ser filtrada, primeira linha deve conter os
            nomes dos campos idênticos aos definidos no nome_campo
            do parâmetro de risco cadastrado.
            OU
            arquivo (str): Arquivo csv de onde carregar a lista a ser filtrada

        Returns:
            lista contendo os campos filtrados. 1ª linha com nomes de campo
        """
        mensagem = 'Arquivo não fornecido!'
        if arquivo:
            mensagem = 'Lista não fornecida!'
            with open(arquivo, 'r', encoding=ENCODE, newline='') as arq:
                reader = csv.reader(arq)
                lista = [linha for linha in reader]
        if not lista:
            raise AttributeError('Erro! ' + mensagem)
        # Precaução: retirar espaços mortos de todo item
        # da lista para evitar erros de comparação
        for ind, linha in enumerate(lista):
            linha_striped = []
            for item in linha:
                if isinstance(item, str):
                    item = item.strip()
                linha_striped.append(item)
            lista[ind] = linha_striped
        # Aplicar pre_processers
        for key in self.pre_processers:
            self.pre_processers[key](lista,
                                     **self.pre_processers_params[key])
        headers = set(lista[0])
        # print('Ativos:', parametros_ativos)
        if parametros_ativos:
            riscos = set(parametros_ativos)
        else:
            riscos = set(list(self._riscosativos.keys()))
        aplicar = headers & riscos   # INTERSECTION OF SETS
        result = []
        result.append(lista[0])
        # print(aplicar)
        # print(self._riscosativos)
        for campo in aplicar:
            dict_filtros = self._riscosativos.get(campo)
            for tipo_filtro, lista_filtros in dict_filtros.items():
                filter_function = filter_functions.get(tipo_filtro)
                if filter_function is None:
                    raise NotImplementedError('Função de filtro' +
                                              tipo_filtro.name +
                                              ' não implementada.')
                result_filter = filter_function(lista, campo, lista_filtros)
                # print('result_filter', result_filter)
                for linha in result_filter:
                    result.append(linha)
        return result

    def parametro_tocsv(self, campo, path=tmpdir):
        """Salva os valores do parâmetro de risco em um arquivo csv
        no formato 'valor', 'tipo_filtro'"""
        lista = []
        lista.append(('valor', 'tipo_filtro'))
        dict_filtros = self._riscosativos.get(campo)
        if dict_filtros is None:
            return False
        for tipo_filtro, lista_filtros in dict_filtros.items():
            for valor in lista_filtros:
                lista.append((valor, tipo_filtro.name))
        filename = os.path.join(path, campo + '.csv')
        with open(filename,
                  'w', encoding=ENCODE, newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lista)
        return filename

    def parametros_tocsv(self, path=tmpdir):
        """Salva os parâmetros adicionados a um gerente em um arquivo csv
        Ver também: :py:func:`parametros_fromcsv`
        """
        for campo in self._riscosativos:
            self.parametro_tocsv(campo, path=path)

    def parametros_fromcsv(self, campo, session=None, padraorisco=None,
                           lista=None, path=tmpdir):
        """
        Abre um arquivo csv, recupera parâmetros configurados nele,
        adiciona à configuração do gerente e **também adiciona ao Banco de
        Dados ativo** caso não existam nele ainda. Para isso é preciso
        passar a session como parâmetro, senão cria apenas na memória
        Pode receber uma lista no lugar de um arquivo csv (como implementado
        em import_named_csv)

        Ver também:

        :py:func:`parametros_tocsv`
        :py:func:`import_named_csv`

        Args:
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
                      'r', encoding=ENCODE, newline='') as f:
                reader = csv.reader(f)
                lista = [linha for linha in reader]
                lista = lista[1:]
        if session:
            parametro = session.query(ParametroRisco).filter(
                ParametroRisco.nome_campo == campo).first()
            if not parametro:
                parametro = ParametroRisco(campo, padraorisco=padraorisco)
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
            self._riscosativos[campo] = dict_filtros

    def import_named_csv(self, arquivo, session=None, padraorisco=None,
                         filtro=Filtro.igual):
        """Abre um arquivo csv, cada coluna sendo um filtro.
        A primeira linha contém o campo a ser filtrado e as linhas
        seguintes os valores do filtro. Cria filtros na memória, e no
        Banco de Dados caso session seja informada.

        Args:
            arquivo: Nome e caminho do arquivo .csv
            session: sessão ativa com BD
            filtro: Tipo de filtro a ser assumido como padrão

        """
        with open(arquivo, 'r', encoding=ENCODE, newline='') as f:
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
            self.parametros_fromcsv(key, session, padraorisco, value)

    def aplica_juncao(self, visao, path=tmpdir, filtrar=False,
                      parametros_ativos=None):
        numero_juncoes = len(visao.tabelas)
        tabela = visao.tabelas[numero_juncoes - 1]
        filhofilename = os.path.join(path, tabela.csv)
        dffilho = pd.read_csv(filhofilename, encoding=ENCODE,
                              dtype=str)
        if hasattr(tabela, 'type'):
            how = tabela.type
        else:
            how = 'inner'
        # print(tabela.csv, tabela.estrangeiro, tabela.primario)
        # A primeira precisa ser "pulada", sempre é a junção 2 tabelas
        # de cada vez. Se numero_juncoes for >2, entrará aqui fazendo
        # a junção em cadeia desde o último até o primeiro filho
        for r in range(numero_juncoes - 2, 0, -1):
            paifilhofilename = os.path.join(path, visao.tabelas[r].csv)
            dfpaifilho = pd.read_csv(paifilhofilename, encoding=ENCODE,
                                     dtype=str)
            # print(tabela.csv, tabela.estrangeiro, tabela.primario)
            dffilho = dfpaifilho.merge(dffilho, how=how,
                                       left_on=tabela.primario,
                                       right_on=tabela.estrangeiro)
            tabela = visao.tabelas[r]
            paifilhofilename = os.path.join(path, tabela.csv)
            if hasattr(tabela, 'type'):
                how = tabela.type
            else:
                how = 'inner'
        csv_pai = visao.tabelas[0].csv
        paifilename = os.path.join(path, csv_pai)
        dfpai = pd.read_csv(paifilename, encoding=ENCODE, dtype=str)
        dfpai = dfpai.merge(dffilho, how=how,
                            left_on=tabela.primario,
                            right_on=tabela.estrangeiro)
        if visao.colunas:
            colunas = [coluna.nome for coluna in visao.colunas]
            result_df = dfpai[colunas]
            result_list = [colunas]
        else:
            result_df = dfpai
            result_list = [result_df.columns.tolist()]
        result_list.extend(result_df.values.tolist())
        if filtrar:
            return self.aplica_risco(result_list,
                                     parametros_ativos=parametros_ativos)
        return result_list
