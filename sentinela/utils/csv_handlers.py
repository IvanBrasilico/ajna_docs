"""Classes para reunir tarefas repetitivas com arquivos csv e planilhas

Padrão do arquivo csv usado é o mais simples possível:
Nomes de campo na primeira linha
Valores nas restantes
Único separador é sempre a vírgula
Fim de linha significa nova linha
Para comparações, retira espaços antes e depois do conteúdo das colunas
"""
import csv
import glob
import io
import os
import tempfile
import unicodedata
from zipfile import ZipFile

tmpdir = tempfile.mkdtemp()
ENCODE = 'latin1'


def ascii_sanitizar(text):
    """Remove espaços à direita e esquerda, espaços adicionais entre
    palavras e marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado
    """
    return unicodedata.normalize('NFKD', text) \
        .encode('ASCII', 'ignore') \
        .decode('ASCII')


def unicode_sanitizar(text):
    """Remove espaços à direita e esquerda, espaços adicionais entre
    palavras e marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado
    """
    norm_txt = unicodedata.normalize('NFD', text)
    shaved = ''.join(char for char in norm_txt
                     if not unicodedata.combining(char))
    return unicodedata.normalize('NFC', shaved)


def sanitizar(text, norm_function=unicode_sanitizar):
    """Remove espaços à direita e esquerda, espaços adicionais entre
    palavras e marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado
    """
    text = text.strip()
    text = text.casefold()
    text = norm_function(text)
    word_list = text.split()
    text = ' '.join(word.strip() for word in word_list
                    if len(word.strip()))
    return text


def muda_titulos_csv(csv_file, de_para_dict):
    """Apenas abre o arquivo e repassa para muda_titulos_lista"""
    with open(csv_file, 'r', encoding=ENCODE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        result = [linha for linha in reader]
    print(result)
    result = muda_titulos_lista(result, de_para_dict)
    print(result)
    return result


def muda_titulos_lista(lista, de_para_dict):
    """Recebe um dicionário na forma titulo_old:titulo_new
    e muda a linha de titulo."""
    cabecalho = []
    for titulo in lista[0]:
        # Se título não está no de_para, retorna ele mesmo
        titulo = sanitizar(titulo)
        novo_titulo = de_para_dict.get(titulo, titulo)
        cabecalho.append(novo_titulo)
    result = [cabecalho]
    result.append(lista[1:])
    return result


def sch_tocsv(sch, txt, dest_path=tmpdir):
    """Pega um arquivo txt, aplica os cabecalhos e a informação de um sch,
    e o transforma em um csv padrão"""
    cabecalhos = []
    for ind in range(len(sch)):
        if not isinstance(sch[ind], str):
            sch[ind] = str(sch[ind], ENCODE)
        linha = sch[ind]
        position_equal = linha.find('="')
        position_quote = linha.find('" ')
        position_col = linha.find('Col')
        if position_equal != -1 and position_col == 0:
            cabecalhos.append(linha[position_equal + 2:position_quote])
    campo = str(sch[0])[2:-3]
    filename = os.path.join(dest_path, campo + '.csv')
    with open(filename, 'w', encoding=ENCODE, newline='') as out:
        writer = csv.writer(out, quotechar='"', quoting=csv.QUOTE_ALL)
        del txt[0]
        writer.writerow(cabecalhos)
        for row in txt:
            if row:
                writer.writerow(row)

    return filename
    # print(sch, txt)


def sch_processing(path, mask_txt='0.txt', dest_path=tmpdir):
    """Processa lotes de extração que gerem arquivos txt csv e arquivos sch
    (txt contém os dados e sch descreve o schema), transformando-os em arquivos
    csv estilo "planilha", isto é, primeira linha de cabecalhos
    path: diretório ou arquivo .zip onde estão os arquivos .sch
    Obs: não há procura recursiva, apenas no raiz do diretório"""
    filenames = []
    if path.find('.zip') == -1:
        for sch in glob.glob(path + '*.sch'):
            sch_name = sch
            txt_name = glob.glob(os.path.join(
                path, '*' + os.path.basename(sch_name)[3:-4] + mask_txt))[0]
            with open(sch_name, encoding=ENCODE,
                      newline='') as sch_file, \
                    open(txt_name, encoding=ENCODE,
                         newline='') as txt_file:
                sch_content = sch_file.readlines()
                reader = csv.reader(txt_file, dialect='excel-tab')
                txt_content = [linha for linha in reader]
                ### RETIFICAR LINHAS!!!!
                # Foram detectados arquivos com falha
                # (TABs a mais, ver notebook ExploraCarga)
                width_header = len(txt_content[0])
                for ind, linha in enumerate(txt_content):
                    width_linha = len(linha)
                    while width_linha > width_header:
                        # Caso haja colunas "sobrando" na linha, retirar
                        # uma coluna nula
                        for index, col in enumerate(linha):
                            if isinstance(col, str) and not col:
                                width_linha -= 1
                                linha.pop(index)
                                break
                csv_name = sch_tocsv(sch_content, txt_content, dest_path)
                filenames.append((csv_name, txt_name))
    else:
        with ZipFile(path) as myzip:
            info_list = myzip.infolist()
            for info in info_list:
                if info.filename.find('.sch') != -1:
                    sch_name = info.filename
                    txt_search = sch_name[3:-4] + mask_txt
                    for txtinfo in info_list:
                        if txtinfo.filename.find(txt_search) != -1:
                            txt_name = txtinfo.filename
                            with myzip.open(sch_name) as sch_file:
                                sch_content = io.TextIOWrapper(
                                    sch_file,
                                    encoding=ENCODE, newline=''
                                ).readlines()
                            with myzip.open(txt_name) as txt_file:
                                txt_io = io.TextIOWrapper(
                                    txt_file,
                                    encoding=ENCODE, newline=''
                                )
                                reader = csv.reader(txt_io, delimiter='\t')
                                txt_content = [linha for linha in reader]

                                print('CONTENT', txt_content[:3])
                    csv_name = sch_tocsv(sch_content, txt_content, dest_path)
                    filenames.append((csv_name, txt_name))
    return filenames
