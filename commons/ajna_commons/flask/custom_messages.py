"""Módulo para configurar Flask - mensagens.

Configurar mensagens personalizadas, em português, no Flask e nos módulos
utilizados, se necessário.
"""

from flask import render_template
from flask_wtf.csrf import CSRFError

#  http://flask.pocoo.org/docs/0.12/patterns/packages/


def configure(blueprint):
    """Recebe blueprint, configura mensagens de erro para aplicação.

    Note-se que as mensages de erro são implementadas no blueprint commons.
    Para que toda a aplicação use os handlers em vez de apenas o blueprint,
    o flask fornece o decorador app_errorhandler em vez do error_handler.

    """
    @blueprint.app_errorhandler(CSRFError)
    def handle_csrf_error(e):
        """Mensagem de erro quando CSRF for encontrado."""
        return render_template('CSRF.html', reason=e.description), 400

    @blueprint.app_errorhandler(404)
    def page_not_found(e):
        """Mensagem de erro quando CSRF for encontrado."""
        return render_template('404.html', reason=e.description), 400
