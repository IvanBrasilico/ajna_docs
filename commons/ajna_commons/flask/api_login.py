"""Funções e views que dão suporte ao LOGIN dos endpoints de API

Classes para acessar os usuários do Banco de Dados
Views padrão login e logout (Flask)
Funções e classes para gerenciar login e usuários (Flask Login)

DBUser.dbsession deve receber a conexão com o BD.

"""
from urllib.parse import urljoin, urlparse

from ajna_commons.flask.log import logger
from ajna_commons.utils.sanitiza import mongo_sanitizar
from flask import (Blueprint, Flask, abort, flash, redirect,
                   render_template, request, url_for)
# from urllib.parse import urlparse, urljoin
from werkzeug.security import check_password_hash, generate_password_hash

from flask_httpauth import HTTPBasicAuth



def configure(app: Flask):
    """Insere as views de login e logout na api.

    Para utilizar, importar modulo api_login e chamar configure(app)
    em uma aplicação Flask.

    """
    auth = HTTPBasicAuth()
    api = Blueprint('api', __name__)

    @api.route('/api/login', methods=['POST'])
    def login():
        """Endpoint para efetuar login (obter token)."""
        pass

    @api.route('api/logout')
    def logout():
        """Endpoint para efetuar logout (Expirar token)."""
        pass

    @app.route('/api/resource')
    @auth.login_required
    def get_resource():
        return jsonify({'data': 'Hello, %s!' % g.user.username})

    @auth.verify_password
    def verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True

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

    app.register_blueprint(api)
