"""Funções e views que dão suporte ao LOGIN das aplicações centralizadas.

Views padrão login e logout (Flask)
Funções e classes para gerenciar login e usuários (Flask Login)

"""
from urllib.parse import urljoin, urlparse

import ajna_commons.flask.custom_messages as custom_messages
from ajna_commons.flask.log import logger
from ajna_commons.flask.user import User
from ajna_commons.utils.sanitiza import mongo_sanitizar
from flask import (Blueprint, Flask, abort, flash, redirect,
                   render_template, request, url_for)
from flask_login import (current_user, LoginManager, login_required,
                         login_user, logout_user)


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
