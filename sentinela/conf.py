import os
import pickle
import tempfile

CSV_DOWNLOAD = 'sentinela/files/'
APP_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_PATH, 'files')
CSV_FOLDER = os.path.join(APP_PATH, 'CSV')
CSV_FOLDER_TEST = os.path.join(APP_PATH, 'tests/CSV')
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'zip'])
tmpdir = tempfile.mkdtemp()
ENCODE = 'latin1'

try:
    SECRET = None
    with open('SECRET', 'rb') as secret:
        try:
            SECRET = pickle.load(secret)
        except pickle.PickleError:
            pass
except FileNotFoundError:
    pass

if not SECRET:
    SECRET = os.urandom(24)
    with open('SECRET', 'wb') as out:
        pickle.dump(SECRET, out, pickle.HIGHEST_PROTOCOL)
