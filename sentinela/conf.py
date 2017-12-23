import os
import tempfile

CSV_DOWNLOAD = 'sentinela/files/'
APP_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_PATH, 'files')
CSV_FOLDER = os.path.join(APP_PATH, 'CSV')
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'zip'])
tmpdir = tempfile.mkdtemp()
ENCODE = 'latin1'
