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
import os
import tempfile
import unicodedata
from zipfile import ZipFile

tmpdir = tempfile.mkdtemp()


def sanitizar(text):
    """Remove espaços à direita e esquerda, espaços adicionais entre
    palavras e marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado
    """
    text = text.strip()
    text = text.casefold()
    norm_txt = unicodedata.normalize('NFD', text)
    shaved = ''.join(char for char in norm_txt
                     if not unicodedata.combining(char))
    text = unicodedata.normalize('NFC', shaved)
    word_list = text.split()
    text = ' '.join(word.strip() for word in word_list
                    if len(word.strip()))
    return text


def muda_titulos_csv(csv_file, de_para_dict):
    """Apenas abre o arquivo e repassa para muda_titulos_lista"""
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        result = [linha for linha in reader]
    result = muda_titulos_lista(result, de_para_dict)
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
            sch[ind] = str(sch[ind], 'iso-8859-1')
        linha = sch[ind]
        position_equal = linha.find('="')
        position_quote = linha.find('" ')
        position_col = linha.find('Col')
        if position_equal != -1 and position_col == 0:
            cabecalhos.append(linha[position_equal + 2:position_quote])
    campo = str(sch[0])[2:-3]
    filename = os.path.join(dest_path, campo + '.csv')
    with open(filename, 'w', newline='') as out:
        writer = csv.writer(out)
        del txt[0]
        writer.writerow(cabecalhos)
        for row in txt:
            if not isinstance(row, str):
                row = str(row, 'iso-8859-1')
            row = row.replace('"', '')
            row = row.replace('\r\n', '')
            row = row.replace('\n', '')
            row = row.split('\t')
            if row:
                writer.writerow(row)

    return filename
    # print(sch, txt)


def sch_processing(path, mask_txt='0.txt'):
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
            with open(sch_name, encoding='iso-8859-1',
                      newline='') as sch_file, \
                    open(txt_name, encoding='iso-8859-1',
                         newline='') as txt_file:
                sch_content = sch_file.readlines()
                txt_content = txt_file.readlines()
                csv_name = sch_tocsv(sch_content, txt_content)
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
                                sch_content = sch_file.readlines()
                            with myzip.open(txt_name) as txt_file:
                                txt_content = txt_file.readlines()
                            csv_name = sch_tocsv(sch_content, txt_content)
                            filenames.append((csv_name, txt_name))
    return filenames
