"""Configuration of AJNA modules LOGs.

Aqui são configurados os diversos arquivos e métodos de logs que serão
comuns aos módulos do sistema AJNA.

Todo módulo deve importar este arquivo e usar o objeto logger criado
para gravar eventos importantes.

"""
import logging
import os
import sys

# from raven.handlers.logging import SentryHandler

# from ajna_commons.flask.conf import SENTRY_DSN
SENTRY_DSN = None
FORMAT_STRING = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
sentry_handler = None


class MyFilter(logging.Filter):
    """Log only especified level (not upper levels)."""

    def __init__(self, level):
        """Configura level desejado."""
        self.__level = level

    def filter(self, log_record):
        """Retorna true se filtro no nível configurado."""
        return log_record.levelno <= self.__level


logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'),
                    format=FORMAT_STRING)
logger = logging.getLogger('ajna')
try:
    fn = getattr(sys.modules['__main__'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    if root_path.find('.exe') != -1:
        root_path = os.path.dirname(__file__)
except AttributeError:
    root_path = os.path.dirname(__file__)

log_file = os.path.join(root_path, 'error.log')
print('Fazendo log de erros e alertas no arquivo ', log_file)
error_handler = logging.FileHandler(log_file)

activity_file = os.path.join(root_path, 'access.log')
print('Fazendo log de atividade no arquivo ', activity_file)
activity_handler = logging.FileHandler(activity_file)

out_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    fmt=FORMAT_STRING,
    datefmt='%Y-%m-%d %H:%M')
error_handler.setFormatter(formatter)
activity_handler.setFormatter(formatter)
out_handler.setFormatter(formatter)
error_handler.setLevel(logging.WARNING)
activity_handler.setLevel(logging.INFO)
logger.addHandler(activity_handler)
logger.addHandler(error_handler)

if os.environ.get('DEBUG', 'None') == '1':
    logger.setLevel(logging.DEBUG)
else:
    out_handler.setLevel(logging.INFO)
    """
    if SENTRY_DSN:
        sentry_handler = SentryHandler(SENTRY_DSN)
        sentry_handler.setFormatter(formatter)
        sentry_handler.setLevel(logging.WARNING)
        sentry_handler.setFormatter(formatter)
        logger.addHandler(sentry_handler)
    """
    logger.setLevel(logging.INFO)
    # Only show info, not warnings, erros, or critical in this log
# logger.addHandler(out_handler)

activity_handler.addFilter(MyFilter(logging.INFO))
logger.info('Configuração de log efetuada')

if __name__ == '__main__':
    logger.debug('TESTE DE LOG')
    logger.warning('TESTE DE LOG')
    logger.error('TESTE DE LOG')
