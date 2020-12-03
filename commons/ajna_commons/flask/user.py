"""Classes que dão suporte ao LOGIN e gerenciamento de Usuários.

Classes para acessar os usuários das aplicações
DBUser.dbsession deve receber a conexão com o BD.

"""
from enum import Enum

import pymongo
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ajna_commons.flask.log import logger
from ajna_commons.utils.sanitiza import mongo_sanitizar


class DBType(Enum):
    mongo = 1
    sqlalchemy = 2


class UserDBComunication():
    def __init__(self, dbsession, alchemy_class=None):
        self.dbsession = dbsession
        if isinstance(dbsession, pymongo.database.Database):
            self.type = DBType.mongo
        else:
            self.type = DBType.sqlalchemy
        self.alchemy_class = alchemy_class

    def insert(self, username, encripted, password):
        if self.type == DBType.mongo:
            cursor = self.dbsession.users.update_one(
                {'username': username},
                {"$set": {'username': username,
                          'password': encripted}},
                upsert=True)
            logger.debug('cursor', cursor)
        elif self.type == DBType.sqlalchemy:
            user = self.dbsession.query(self.alchemy_class). \
                filter(self.alchemy_class.cpf == username).one_or_none()
            if user is None:
                user = self.alchemy_class()
                user.cpf = username
            user.password = password
            self.dbsession.add(user)
            self.dbsession.commit()

    def update(self, username, encripted, password):
        if self.type == DBType.mongo:
            cursor = self.dbsession.users.update_one(
                {'username': username},
                {"$set": {'username': username,
                          'password': encripted}},
                upsert=True)
            logger.debug('cursor', cursor)
        elif self.type == DBType.sqlalchemy:
            user = self.dbsession.query(self.alchemy_class). \
                filter(self.alchemy_class.cpf == username).one()
            user.password = password
            self.dbsession.add(user)
            self.dbsession.commit()

    def get(self, username):
        user = None
        if self.type == DBType.mongo:
            user = self.dbsession.users.find_one(
                {'username': username})
        elif self.type == DBType.sqlalchemy:
            user = None
            usuario = self.dbsession.query(self.alchemy_class). \
                filter(self.alchemy_class.cpf == username).one_or_none()
            if usuario:
                user = {'password': usuario.password, 'nome': usuario.nome}
        return user


class DBUser():
    """Classe que valida o usuário em uma base.

    A conexão à base deve ser informada antes do uso da classe.
    Se dbsession for None, get retorna usuario caso username==senha
    (Comportamento utilizado para testes unitários)
    Podem ser passadas outras conexões a outros BD caso implementem os métodos
    users.update e users.find_one, ou criada uma classe descendente de
    DBUser que modifique os métodos get e add.

    A maioria dos métodos são estáticos, sendo usados diretamente:

    DBUser.dbsession = meu_PyMongoClient
    DBUser.get(usuario, senha) retorna DBUSer se existir e se senha correta
    DBUser.add(usuario, senha) adiciona DBUser

    A classe DBUser é utilizada pela classe User, padrão do flask-login

    """

    dbsession = None
    alchemy_class = None

    def __init__(self, id, password=None):
        """Apenas monta uma instância."""
        self.id = id
        self.name = str(id)
        self._password = password

    @classmethod
    def sanitize(cls, username, password):
        """Sanitização das entradas."""
        return mongo_sanitizar(username), mongo_sanitizar(password)

    @classmethod
    def add(cls, username, password):
        """Cria usuário ou muda senha se ele existe."""
        if not cls.dbsession:
            raise Exception('Sem conexão com o Banco de Dados!')
        username, password = cls.sanitize(username, password)
        encripted = cls.encript(password)
        dbcomunicator = UserDBComunication(cls.dbsession, cls.alchemy_class)
        dbcomunicator.insert(username, encripted, password)
        return DBUser.get(username, password)

    @classmethod
    def change_password(cls, username, password):
        """Cria usuário ou muda senha se ele existe."""
        if not cls.dbsession:
            raise Exception('Sem conexão com o Banco de Dados!')
        username, password = cls.sanitize(username, password)
        encripted = cls.encript(password)
        dbcomunicator = UserDBComunication(cls.dbsession, cls.alchemy_class)
        dbcomunicator.insert(username, encripted, password)
        return True

    @classmethod
    def encript(cls, password):
        """Recebe senha plana, retorna versão criptografada."""
        if password is None:
            return ''
        return generate_password_hash(password)

    def check(self, encripted):
        """Verifica senha informada contra a versão criptograda do BD."""
        if self._password is None or encripted is None:
            return False
        return check_password_hash(encripted, self._password)

    @classmethod
    def get(cls, username, password=None):
        """Testa se Usuario existe. Se senha for passada, testa se é válida.

        Retorna instância DBUser se usuário existe e senha válida, None se
        Usuario não encontrado OU senha inválida.

        """
        logger.debug('Getting user. dbsession= %s' % cls.dbsession)
        if cls.dbsession:
            username, password = cls.sanitize(username, password)
            # logger.debug('DBSEssion %s' % cls.dbsession)
            dbuser = DBUser(username, password)
            dbcomunicator = UserDBComunication(cls.dbsession, cls.alchemy_class)
            user = dbcomunicator.get(username)
            if user is None:
                return None
            if password is not None:
                encripted = user['password']
                logger.debug('encripted %s' % encripted)
                if not dbuser.check(encripted):
                    return None
            return DBUser(username, password)
        else:
            if username:
                if (not password) or (username == password):
                    return DBUser(username, password)
        return None


class User(UserMixin):
    """Mixin padrão do flask-login.

    Está utilizando DBUser como base de autenticação.
    Para utilizar outra base de dados, criar outra classe com
    comportamento similar a DBUSer.

    """

    user_database = DBUser

    def __init__(self, id):
        """Instancia User."""
        self.id = id
        self.name = str(id)

    def change_password(self, newpassword):
        self.user_database.change_password(self.id, newpassword)

    @classmethod
    def get(cls, username, password=None):
        """Consulta DBUser."""
        dbuser = cls.user_database.get(username, password)
        if dbuser:
            return User(dbuser.name)
        return None
