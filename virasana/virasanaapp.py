import os
import time

from celery import Celery
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from virasana.workers.raspadir import trata_bson

# initialize constants used for server queuing
BATCH_SIZE = 1000
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# initialize our Flask application, Redis server, and Keras model
app = Flask(__name__)
app.config['DEBUG'] = True
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##########
BACKEND = BROKER = 'redis://localhost:6379'

celery = Celery(app.name, broker=BROKER,
                backend=BACKEND)


@celery.task(bind=True)
def raspadir(self):
    """Background task that go to directory of incoming files
    AND load then to mongodb
    """
    for file in os.listdir(UPLOAD_FOLDER):
        if 'bson' in file:
            trata_bson(file)

    return True
######################


def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['bson', 'bson.zip']


@app.route('/uploadbson', methods=['POST'])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {'success': False, 'progress': 1}
    s0 = None
    # ensure a bson was properly uploaded to our endpoint
    if request.method == 'POST':
        data['progress'] = 2
        file = request.files.get('file')
        data['progress'] = 3
        if file and file.filename != '' and allowed_file(file.filename):
            s0 = time.time()
            print('Enter Sandman - sending request to celery queue')
            filename = secure_filename(file.filename)
            data['progress'] = 4
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            data['progress'] = 5
            raspadir.delay()
            data['progress'] = 6
            data['success'] = True
    # return the data dictionary as a JSON response
    if s0 is not None:
        s1 = time.time()
        print(s1, 'Results read from queue and returned in ', s1 - s0)
    return jsonify(data)


if __name__ == '__main__':
    # start the web server
    print('* Starting web service...')
    app.run()
