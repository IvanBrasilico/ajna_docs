"""Define configurações comuns aos módulos do AJNA.

Exemplos:

    SECRET - chave para criptografia da sessão
    REDIS SERVER
    MONGODB SERVER
    Custom messages- mensagens customizadas para módulos de login, segurança,
    erro, etc
    Configurações de logging, etc

"""
# import logging
import os
import pickle
import tempfile

try:
    import redis
except ImportError:
    pass
# from ajna_commons.flask.log import logger
from dominate.tags import img

tmpdir = tempfile.mkdtemp()
logo = img(src='/static/material_logo.svg', height='40')

try:
    with open('SECRET', 'rb') as secret:
        try:
            SECRET = pickle.load(secret)
        except pickle.PickleError:
            SECRET = None
except FileNotFoundError:
    SECRET = None

if SECRET is None:
    SECRET = os.urandom(24)
    with open('SECRET', 'wb') as out:
        pickle.dump(SECRET, out, pickle.HIGHEST_PROTOCOL)

PADMA_REDIS = 'PADMA_REDIS'
BSON_REDIS = 'bson'
REDIS_URL = os.environ.get('REDIS_URL')
if not REDIS_URL:
    REDIS_URL = 'redis://localhost:6379'
BACKEND = BROKER = REDIS_URL
try:
    redisdb = redis.StrictRedis.from_url(REDIS_URL)
except NameError:
    pass

MONGODB_URI = os.environ.get('MONGODB_URI')
if MONGODB_URI:
    DATABASE = ''.join(MONGODB_URI.rsplit('/')[-1:])
    # print(DATABASE)
else:
    DATABASE = 'test'

SQL_URI = os.environ.get('SQL_URI', 'mysql+pymysql://ivan@localhost:3306/mercante')

SENTRY_DSN = os.environ.get('SENTRY_DSN')

# initialize constants used for server queuing
TIMEOUT = 10
BATCH_SIZE = 1000
ALLOWED_EXTENSIONS = set(['csv', 'zip', 'txt', 'png', 'jpg', 'jpeg', 'sch'])

# Address of MicroServices from ajna modules
# Devem ser definidas em variáveis de ambiente no Servidor de Deploy
# o wsgi_debug utilizará estes, fixos
BHADRASANA_URL = os.environ.get('BHADRASANA_URL')
if not BHADRASANA_URL:
    BHADRASANA_URL = 'http://localhost:5000'
VIRASANA_URL = os.environ.get('VIRASANA_URL')
if not VIRASANA_URL:
    VIRASANA_URL = 'http://localhost:5001'
PADMA_URL = os.environ.get('PADMA_URL')
if not PADMA_URL:
    PADMA_URL = 'http://localhost:5002'
