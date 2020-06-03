"""Funções e views que dão suporte ao LOGIN dos endpoints de API

Funções e classes para gerenciar login e tokens (Flask jwt)

"""
from ajna_commons.flask.conf import SECRET
from ajna_commons.flask.log import logger
from ajna_commons.flask.login import authenticate
from ajna_commons.flask.user import User
from ajna_commons.utils.sanitiza import mongo_sanitizar
from flask import Blueprint, Flask, jsonify
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)


def configure(app: Flask):
    """Insere as views de login e logout na api.

    Para utilizar, importar modulo api_login e chamar configure(app)
    em uma aplicação Flask.

    """
    api = Blueprint('/api', __name__)
    app.config['JWT_SECRET_KEY'] = SECRET
    app.config['JWT_BLACKLIST_ENABLED'] = True
    jwt = JWTManager(app)

    blacklist = set()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    @api.route('/api/login', methods=['POST'])
    def login():
        """Endpoint para efetuar login (obter token)."""
        if not request.json or not request.is_json:
            return jsonify({"msg": "JSON requerido"}), 400
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "Parametro username requerido"}), 400
        if not password:
            return jsonify({"msg": "Parametro password requerido"}), 400
        user = verify_password(username, password)
        if user is None:
            return jsonify({"msg": "username ou password invalidos"}), 401
        logger.info('Entrando com usuário %s' % username)
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    @api.route('/api/login_certificado', methods=['GET', 'POST'])
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
                user = User.get(name)
                if user is None:
                    return jsonify(
                        {"msg": "Username invalido (usuário %s não cadastrado" % name}
                    ), 401
                access_token = create_access_token(identity=user.id)
                return jsonify(access_token=access_token), 200
        return jsonify({"msg": "Cabeçalhos com info do certificado não encontrados"}), 401

    @api.route('/api/logout', methods=['DELETE'])
    @jwt_required
    def logout():
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        current_user = get_jwt_identity()
        logger.info('Usuário %s efetuou logout' % current_user)
        return jsonify({"msg": "Logout efetuado"}), 200

    @api.route('/api/test')
    @jwt_required
    def get_resource():
        current_user = get_jwt_identity()
        return jsonify({'user.id': current_user}), 200


    @api.before_request
    def before_request_callback():
        path = None
        method = None
        ip = None
        try:
            current_user = get_jwt_identity()
        except Exception as err:
            logger.info(str(err), exc_info=True)
            current_user = 'no user' + str(err)
        logger.info('Usuário %s' % current_user)

        try:
            path = request.path
            method = request.method
            ip = request.environ.get('HTTP_X_REAL_IP',
                                     request.remote_addr)
        finally:
            logger.info('API LOG url: %s %s IP:%s User: %s' %
                            (path, method, ip, current_user))

    @api.after_request
    def after_request_callback(response):
        before_request_callback()
        return response

    def verify_password(username, password):
        username = mongo_sanitizar(username)
        # Não aceitar senha vazia!!
        password = mongo_sanitizar(password)
        user = authenticate(username, password)
        if user is not None:
            logger.info('Usuário %s %s autenticou via API' %
                        (user.id, user.name))
        return user

    app.register_blueprint(api)
    return api
