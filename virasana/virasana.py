import io
import time
import os

from celery import Celery
from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename

from image_aq.models.bsonimage import BsonImage, BsonImageList
from virasana.workers.raspadir import raspadir

# initialize constants used for server queuing
BATCH_SIZE = 1000
UPLOAD_FOLDER = 'virasana/static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# initialize our Flask application, Redis server, and Keras model
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['bson', 'bson.zip']

@app.route('/uploadbson', methods=['POST'])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {'success': False}
    s0 = None
    # ensure a bson was properly uploaded to our endpoint
    if request.method == 'POST':
        file = request.files.get('files')
        if file and file.filename != '' and allowed_file(file.filename):
            s0 = time.time()
            print('Enter Sandman - sending request to celery queue')
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            raspadir.delay()
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
