import io
import json
import falcon
import numpy as np
import random
import bson
from PIL import Image
from wsgiref import simple_server

from pymongo import MongoClient
from gridfs import GridFS


db = MongoClient(host='localhost')['test']
fs = GridFS(db)

lista_ids = [
    linha['_id'] for linha in
    db['fs.files'].find(
        {'metadata.contentType': 'image/jpeg'}, {'_id': 1}
    ).limit(1000)
]


def recorta_imagem(grid_out, mini):
    preds = grid_out.metadata.get('predictions')
    if preds:
        bboxes = [pred.get('bbox') for pred in preds]
    n = int(mini)
    if len(bboxes) >= n + 1 and bboxes[n]:
        coords = bboxes[n]
        pil_image = Image.open(io.BytesIO(grid_out.read()))
        pil_image = pil_image.crop((coords[1], coords[0], coords[3], coords[2]))
        image_bytes = io.BytesIO()
        pil_image.save(image_bytes, 'JPEG')
        image_bytes.seek(0)
        return image_bytes.read()
    print('Não achou bbox...')
    return None


def mongo_image(image_id, mini=None):
    """Lê imagem do Banco MongoDB. Retorna None se ID não encontrado."""
    try:
        _id = bson.ObjectId(image_id)
        if fs.exists(_id):
            grid_out = fs.get(_id)
            if mini is None:
                image = grid_out.read()
            else:
                image = recorta_imagem(grid_out, mini)
            return image
    except bson.errors.InvalidId as err:
        print(err)
    return None


class ImageResource(object):
    def __init__(self, image_loader):
        self.image_loader = image_loader

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JPEG
        _id = req.get_param('id')
        mini = req.get_param('mini')
        if _id is None:
            _id = lista_ids[random.randint(0, 100)]
        # print('_id', _id)
        # print('mini', mini)
        resp.data = self.image_loader(_id, mini)
        if resp.data is None:
            print("Retornando None...")


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
images = ImageResource(mongo_image)


# things will handle all requests to the '/things' URL path
app.add_route('/img', images)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
