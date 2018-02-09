import os
import time

from celery import Celery, states
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from virasana.workers.raspadir import trata_bson

# initialize constants used for server queuing
TIMEOUT = 10
BATCH_SIZE = 1000
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# initialize our Flask application, Redis server, and Keras model
app = Flask(__name__)
app.config['DEBUG'] = True
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# TODO: put in separate file
BACKEND = BROKER = 'redis://localhost:6379'

celery = Celery(app.name, broker=BROKER,
                backend=BACKEND)


@celery.task(bind=True)
def raspa_dir(self):
    """Background task that go to directory of incoming files
    AND load then to mongodb
    """
    self.update_state(state=states.STARTED,
                      meta={'current': '',
                            'status': 'Iniciando'})
    for file in os.listdir(UPLOAD_FOLDER):
        self.update_state(state=states.STARTED,
                          meta={'current': file,
                                'status': 'Processando arquivos...'})
        if 'bson' in file:
            trata_bson(file)
        os.remove(os.path.join(UPLOAD_FOLDER, file))
    return {'current': '',
            'status': 'Todos os arquivos processados'}
######################


def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['bson', 'bson.zip']


@app.route('/uploadbson', methods=['POST'])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {'progress': 'Function predict called'}
    s0 = None
    # ensure a bson was properly uploaded to our endpoint
    if request.method == 'POST':
        data['progress'] = 'Post checked'
        file = request.files.get('file')
        if file and file.filename != '' and allowed_file(file.filename):
            data['progress'] = 'File checked'
            s0 = time.time()
            print('Enter Sandman - sending request to celery queue')
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            data['progress'] = 'File uploaded'
            task = raspa_dir.delay()
            data['progress'] = 'Task initiated'
            # Wait 10s for celery to return success or failure
            for r in range(1, 50):
                time.sleep(TIMEOUT / 50)
                if task.state in states.READY_STATES:
                    data['progress'] = 'Task ended'
                    break
            if task.state not in states.READY_STATES:
                data['progress'] = (
                    'Timeout! Checar se serviço Celery está '
                    'rodando e se não está travado. A tarefa pode '
                    ' estar também demorando muito tempo para executar. \n '
                    'task celery raspa_dir \n '
                    'Timeout configurado para ' + str(TIMEOUT) + 's')

    # return the data dictionary as a JSON response
    if s0 is not None:
        s1 = time.time()
        print(s1, 'Results read from queue and returned in ', s1 - s0)
    if task and task.info:
        data['state'] = task.state
        data = {**data, **task.info}
    return jsonify(data)


if __name__ == '__main__':
    # start the web server
    print('* Starting web service...')
    app.run()
