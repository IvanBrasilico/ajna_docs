"""Classes para reunir tarefas repetitivas com arquivos csv
e planilhas"""
import csv
import os
import glob
from zipfile import ZipFile, ZipInfo


def muda_titulos_csv(csv_file, de_para_dict):
    """Apenas abre o arquivo e repassa para muda_titulos_lista"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        result = [linha for linha in reader]
    result = muda_titulos_lista(result, de_para_dict)
    return result


def muda_titulos_lista(lista, de_para_dict):
    """Recebe um dicionário na forma titulo_old:titulo_new
    e muda a linha de titulo."""
    cabecalho = []
    for titulo in lista[0]:
        # Se título não está no de_para, retorna ele mesmo
        titulo = titulo.strip()
        novo_titulo = de_para_dict.get(titulo, titulo)
        cabecalho.append(novo_titulo)
    result = [cabecalho]
    result.append(lista[1:])
    return result


def sch_tocsv(sch, txt):
    print(sch, txt)


def sch_processing(path, mask_txt='0.txt'):
    """Processa lotes de extração que gerem arquivos txt csv e arquivos sch
    (txt contém os dados e sch descreve o schema), transformando-os em arquivos
    csv estilo "planilha", isto é, primeira linha de cabecalhos
    path: diretório ou arquivo .zip onde estão os arquivos .sch
    Obs: não há procura recursiva, apenas no raiz do diretório"""
    if path.find('.zip') == -1:
        for sch in glob.glob(path + '*.sch'):
            sch_name = os.path.basename(sch)
            txt = glob.glob(os.path.join(
                path, '*' + sch_name[3:-4] + mask_txt))[0]
            sch_tocsv(sch, txt)
    else:
        with ZipFile(path) as myzip:
            info_list = myzip.infolist()
            for info in info_list:
                if info.filename.find('.sch'):
                    txt_search = sch_name[3:-4] + mask_txt
                    for info in info_list:
                        if info.filename.find(txt_search):
                            sch_tocsv(sch, txt)
