# Código do celery task está no arquivo principal virasana.virasana.py
# TODO: resolver circular import para ativar este arquivo e deixar
# código que cria a task Celery separado neste arquivo
import os

import gridfs
from pymongo import MongoClient

from image_aq.models.bsonimage import BsonImageList

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static')


def trata_bson(bson_file):
    db = MongoClient().test
    fs = gridfs.GridFS(db)
    bsonimagelist = BsonImageList.fromfile(
        os.path.join(UPLOAD_FOLDER, bson_file))
    files_ids = bsonimagelist.tomongo(fs)
    return files_ids
