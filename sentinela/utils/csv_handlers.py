"""Classes para reunir tarefas repetitivas com arquivos csv
e planilhas"""
import csv


def muda_titulos_csv(csv_file, de_para_dict):
    """Apenas abre o arquivo e repassa para muda_titulos_lista"""
    with open(csv_file, 'r') as f:
        result = f.readlines()
    muda_titulos_lista(result, de_para_dict)
    return result


def muda_titulos_lista(lista, de_para_dict):
    """Recebe um dicionário na forma titulo_old:titulo_new
    e muda a linha de titulo."""
    for old, new in de_para_dict.items():
        print(old, new)
        lista[0] = lista[0].replace(old, new)
