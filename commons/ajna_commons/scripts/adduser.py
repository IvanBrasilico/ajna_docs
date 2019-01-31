"""Um script simples para adicionar um usuário ao BD.

Uso:
   python ajna_commons/scripts/adduser.py -u=username -p=password

"""
import click
from pymongo import MongoClient

from ajna_commons.flask.conf import DATABASE, MONGODB_URI
from ajna_commons.flask.login import DBUser


@click.command()
@click.option('-u', help='Nome de usuário', prompt='Digite o nome de usuário')
@click.option('-p', help='Senha', prompt='Agora digite a senha')
def adduser(u, p):
    """Insere usuário no Banco de Dados ou atualiza senha."""
    db = MongoClient(host=MONGODB_URI)[DATABASE]
    DBUser.dbsession = db
    return DBUser.add(u, p)


if __name__ == '__main__':
    print(adduser())
