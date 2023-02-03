"""Funções e views que dão suporte ao LOGIN das aplicações centralizadas.

Views padrão login e logout (Flask)
Funções e classes para gerenciar login e usuários (Flask Login)

"""
from urllib.parse import urljoin, urlparse

from flask import (Blueprint, Flask, abort, flash, redirect,
                   render_template, request, url_for)
from flask_login import (current_user, LoginManager, login_required,
                         login_user, logout_user)

import ajna_commons.flask.custom_messages as custom_messages
from ajna_commons.flask.log import logger
from ajna_commons.flask.user import User
from ajna_commons.utils.sanitiza import mongo_sanitizar

login_manager = LoginManager()
login_manager.login_view = '/login'


def login_view(request):
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


def configure(app: Flask):
    """Insere as views de login e logout na app.

    Para utilizar, importar modulo login e chamar configure(app)
    em uma aplicação Flask.

    """
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    commons = Blueprint('commons', __name__, template_folder='templates')
    custom_messages.configure(commons)

    @commons.route('/login', methods=['GET', 'POST'])
    # @commons.route('/virana/login', methods=['GET', 'POST'])
    # @commons.route('/bhadrasana2/login', methods=['GET', 'POST'])
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

    @commons.route('/login_certificado', methods=['GET'])
    @commons.route('/virasana/login_certificado', methods=['GET'])
    @commons.route('/bhadrasana/login_certificado', methods=['GET'])
    @commons.route('/bhadrasana2/login_certificado', methods=['GET'])
    def login_certificado():
        """View para efetuar login via certificado digital."""
        s_dn = request.environ.get('HTTP_SSL_CLIENT_S_DN')
        logger.info('URL %s - s_dn %s' % (request.url, s_dn))
        if s_dn:
            name = None
            names = dict([x.split('=') for x in s_dn.split(',')])
            logger.info('name %s' % names)
            if names:
                name = names.get('CN').split(':')[-1]
            logger.info('%s ofereceu certificado digital' % name)
            if name:
                name = name.strip().lower()
                registered_user = User.get(name)
                if registered_user is not None:
                    flash('Usuário autenticado.')
                    login_user(registered_user)
                    logger.info('Usuário %s autenticou' % current_user.name)
                    return redirect(url_for('index'))
                else:
                    flash('Usuário não encontrado %s' % name)
                    return abort(404)
        flash('Certificado não encontrado %s' % s_dn)
        return abort(401)

    def get_next_url_login(message=''):
        next_url = url_for('commons.login', message=message)
        print(next_url)
        parts = next_url.split('/')  # Eliminar caminho base se repetido
        print(parts)
        cleaned_parts = []
        for part in parts:
            if part not in cleaned_parts:
                cleaned_parts.append(part)
        print(cleaned_parts)
        return '/'.join(cleaned_parts)

    @commons.route('/logout')
    @login_required
    def logout():
        """View para efetuar logout."""
        logout_user()
        next = request.args.get('next')
        if not is_safe_url(next):
            next = None
        return redirect(get_next_url_login())

    # @login_manager.unauthorized_handler
    @app.errorhandler(401)
    def unauthorized(args):
        """Gerenciador de usuário não autorizado padrão do flask-login."""
        logger.debug(args)
        message = 'Não autorizado! ' + \
                  'Efetue login novamente com usuário e senha válidos.'
        return redirect(get_next_url_login())

    @login_manager.user_loader
    def load_user(userid):
        """Método padrão do flask-login. Repassa responsabilidade a User."""
        user_entry = User.get(userid)
        return user_entry

    app.register_blueprint(commons)


def authenticate(username, password=None):
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
