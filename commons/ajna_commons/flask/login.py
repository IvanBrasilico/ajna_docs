"""Funções e views que dão suporte ao LOGIN das aplicações centralizadas.

Classes para acessar os usuários do Banco de Dados
Views padrão login e logout (Flask)
Funções e classes para gerenciar login e usuários (Flask Login)

DBUser.dbsession deve receber a conexão com o BD.

"""
from urllib.parse import urljoin, urlparse

from flask import (Blueprint, Flask, abort, flash, redirect,
                   render_template, request, url_for)
from flask_login import (current_user, LoginManager, UserMixin, login_required,
                         login_user, logout_user)
# from urllib.parse import urlparse, urljoin
from werkzeug.security import check_password_hash, generate_password_hash

import ajna_commons.flask.custom_messages as custom_messages
from ajna_commons.utils.sanitiza import mongo_sanitizar
from ajna_commons.flask.log import logger


def configure(app: Flask):
    """Insere as views de login e logout na app.

    Para utilizar, importar modulo login e chamar configure(app)
    em uma aplicação Flask.

    """
    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    commons = Blueprint('commons', __name__, template_folder='templates')
    custom_messages.configure(commons)

    @commons.route('/login', methods=['GET', 'POST'])
    def login():
        """View para efetuar login."""
        message = request.args.get('message')
        if request.method == 'POST':
            username = mongo_sanitizar(request.form.get('username'))
            # Não aceitar senha vazia!!
            password = mongo_sanitizar(request.form.get('senha', '*'))
            registered_user = authenticate(username, password)
            if registered_user is not None:
                flash('Usuário autenticado.')
                login_user(registered_user)
                logger.info('Usuário %s autenticou' % current_user.name)
                # g['username'] = current_user.name
                return redirect(url_for('index'))
            else:
                return abort(401)
        else:
            if message:
                flash(message)
            return render_template('login.html', form=request.form)

    @commons.route('/logout')
    @login_required
    def logout():
        """View para efetuar logout."""
        logout_user()
        next = request.args.get('next')
        if not is_safe_url(next):
            next = None
        return redirect(url_for('index'))

    # @login_manager.unauthorized_handler
    @app.errorhandler(401)
    def unauthorized(args):
        """Gerenciador de usuário não autorizado padrão do flask-login."""
        logger.debug(args)
        message = 'Não autorizado! ' + \
            'Efetue login novamente com usuário e senha válidos.'
        return redirect(url_for('commons.login',
                                message=message))

    @login_manager.user_loader
    def load_user(userid):
        """Método padrão do flask-login. Repassa responsabilidade a User."""
        user_entry = User.get(userid)
        return user_entry

    app.register_blueprint(commons)


class DBUser():
    """Classe que valida o usuário em uma base MongoDB.

    A conexão à base MongoDB deve ser informada antes do uso da classe.
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
        cursor = cls.dbsession.users.update_one(
            {'username': username},
            {"$set": {'username': username,
             'password': encripted}},
            upsert=True)
        logger.debug('cursor', cursor)
        return DBUser.get(username, password)

    @classmethod
    def encript(cls, password):
        """Recebe senha plana, retorna versão criptografada."""
        if password is None:
            return ''
        return generate_password_hash(password)

    def check(self, encripted):
        """Verifica senha informada contra a versão criptograda do BD."""
        if self._password is None:
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
            user = cls.dbsession.users.find_one(
                {'username': username})
            if user is None:
                return None
            # logger.debug('***username %s, passed password %s ' % \
            #             (username, password))
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

    @classmethod
    def get(cls, username, password=None):
        """Consulta DBUser."""
        dbuser = cls.user_database.get(username, password)
        if dbuser:
            return User(dbuser.name)
        return None


def authenticate(username, password):
    """Método padrão do flask-login. Repassa responsabilidade a User."""
    if password is None:
        return None
    user_entry = User.get(username, password)
    # logger.debug('authenticate user entry %s' % user_entry)
    return user_entry


def is_safe_url(target):
    """Testa ocorrência de ataque de redirecionamento(URL Redirect/Pishing)."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
