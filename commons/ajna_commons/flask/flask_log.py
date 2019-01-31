"""Configura logs específicos para o Flask."""
import logging
from _datetime import datetime
from flask import request
from flask_login import current_user
from flask.logging import default_handler

import ajna_commons.flask.log as log


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """Adiciona varíaveis de usuário e IP ao log."""
        log_record.utcnow = (datetime.utcnow()
                             .strftime('%Y-%m-%d %H:%M:%S,%f %Z'))
        log_record.url = request.path
        log_record.method = request.method
        # Try to get the IP address of the user through reverse proxy
        log_record.ip = request.environ.get('HTTP_X_REAL_IP',
                                            request.remote_addr)
        if current_user.is_anonymous():
            log_record.user_id = 'guest'
        else:
            log_record.user_id = current_user.get_id()
        return True


def configure_applog(app):
    """Cria logger para o processo web (flask)."""
    # log_format = ('%(utcnow)s\tl=%(levelname)s\tu=%(user_id)s\tip=%(ip)s'
    #               '\tm=%(method)s\turl=%(url)s\tmsg=%(message)s')
    # formatter = logging.Formatter(log_format)
    app.logger.setLevel(logging.DEBUG)
    # app.logger.addFilter(ContextualFilter())
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(log.activity_handler)
    app.logger.addHandler(log.error_handler)
    app.logger.addHandler(log.out_handler)
    wsgi = logging.getLogger('werkzeug')
    wsgi.addHandler(log.activity_handler)
    if log.sentry_handler:
        app.logger.addHandler(log.sentry_handler)

    @app.before_request
    def before_request_callback():
        path = request.path
        method = request.method
        ip = request.environ.get('HTTP_X_REAL_IP',
                                 request.remote_addr)
        try:
            user_name = current_user.name
        except:
            user_name = 'no user'
        app.logger.info('url: %s %s IP:%s User: %s' %
                        (path, method, ip, user_name))
