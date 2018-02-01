# JSON server
# Args
#  model, params
# Returns
#   JSON dict with model response
import io
import json
import time
import uuid
from threading import Thread

import flask
import numpy as np
import redis
from keras.applications import ResNet50, imagenet_utils
from PIL import Image

from app.utils import base64_decode_image, base64_encode_image, prepare_image

# initialize constants used to control image spatial dimensions and
# data type
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_CHANS = 3
IMAGE_DTYPE = 'float32'

# initialize constants used for server queuing
IMAGE_QUEUE = 'image_queue'
BATCH_SIZE = 32
SERVER_SLEEP = 0.20
CLIENT_SLEEP = 0.10


# initialize our Flask application, Redis server, and Keras model
app = flask.Flask(__name__)
app.config['DEBUG'] = True
db = redis.StrictRedis(host='localhost', port=6379, db=0)
model = None


def classify_process():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    print('* Loading model...')
    model = ResNet50(weights='imagenet')
    print('* Model loaded')

    # continually poll for new images to classify
    while True:
        # attempt to grab a batch of images from the database, then
        # initialize the image IDs and batch of images themselves
        queue = db.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
        imageIDs = []
        batch = None
        # loop over the queue
        for q in queue:
            # deserialize the object and obtain the input image
            q = json.loads(q.decode('utf-8'))
            image = base64_decode_image(q['image'], IMAGE_DTYPE,
                                        (1, IMAGE_HEIGHT, IMAGE_WIDTH,
                                         IMAGE_CHANS))
            # check to see if the batch list is None
            if batch is None:
                batch = image
            # otherwise, stack the data
            else:
                batch = np.vstack([batch, image])
            # update the list of image IDs
            imageIDs.append(q['id'])
            # check to see if we need to process the batch
        if len(imageIDs) > 0:
            # classify the batch
            print('* Batch size: {}'.format(batch.shape))
            s0 = time.time()
            print('Processing images classifiers from queue')
            preds = model.predict(batch)
            results = imagenet_utils.decode_predictions(preds)

            # loop over the image IDs and their corresponding set of
            # results from our model
            for (imageID, resultSet) in zip(imageIDs, results):
                # initialize the list of output predictions
                output = []

                # loop over the results and add them to the list of
                # output predictions
                for (imagenetID, label, prob) in resultSet:
                    r = {'label': label, 'probability': float(prob)}
                    output.append(r)

                # store the output predictions in the database, using
                # the image ID as the key so we can fetch the results
                db.set(imageID, json.dumps(output))

            # remove the set of images from our queue
            db.ltrim(IMAGE_QUEUE, len(imageIDs), -1)

            s1 = time.time()
            print(s1, 'Images classified in ', s1 - s0)
        # sleep for a small amount
        time.sleep(SERVER_SLEEP)


@app.route('/predict', methods=['POST'])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {'success': False}
    s0 = None

    # ensure an image was properly uploaded to our endpoint
    print(flask.request.files)
    if flask.request.method == 'POST':
        if flask.request.files.get('image'):
            s0 = time.time()
            print('Enter Sandman - sending request to queue')

            # read the image in PIL format and prepare it for
            # classification
            image = flask.request.files['image'].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image, (IMAGE_WIDTH, IMAGE_HEIGHT))

            # ensure our NumPy array is C-contiguous as well,
            # otherwise we won't be able to serialize it
            image = image.copy(order='C')
            # generate an ID for the classification then add the
            # classification ID + image to the queue
            k = str(uuid.uuid4())
            d = {'id': k, 'image': base64_encode_image(image)}
            db.rpush(IMAGE_QUEUE, json.dumps(d))
            # keep looping until our model server returns the output
            # predictions
            while True:
                # attempt to grab the output predictions
                output = db.get(k)

                # check to see if our model has classified the input
                # image
                if output is not None:
                    # add the output predictions to our data
                    # dictionary so we can return it to the client
                    output = output.decode('utf-8')
                    data['predictions'] = json.loads(output)
                    # delete the result from the database and break
                    # from the polling loop
                    db.delete(k)
                    break
                # sleep for a small amount to give the model a chance
                # to classify the input image
                time.sleep(CLIENT_SLEEP)

            # indicate that the request was a success
            data['success'] = True

    # return the data dictionary as a JSON response
    if s0 is not None:
        s1 = time.time()
        print(s1, 'Results read from queue and returned in ', s1 - s0)
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == '__main__':
    # load the function used to classify input images in a *separate*
    # thread than the one used for main classification
    print('* Starting model service...')
    t = Thread(target=classify_process, args=())
    t.daemon = True
    t.start()

    # start the web server
    print('* Starting web service...')
    app.run()
