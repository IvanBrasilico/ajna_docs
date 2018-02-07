import os
from celery import Celery
import gridfs
from pymongo import MongoClient

from image_aq.models.bsonimage import BsonImage, BsonImageList
from virasana.virasana import app, UPLOAD_FOLDER

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(app.name, broker=BROKER,
                backend=BACKEND)

db = MongoClient().test
fs = gridfs.GridFS(db)

@celery.task(bind=True)
def raspadir(self, dossie_id, refazer=False):
    """Background task that go to directory of incoming files
    AND load then to mongodb
    """
    for file in os.listdir(UPLOAD_FOLDER):
        if 'bson' in file:
            bsonimagelist = BsonImageList.fromfile(file)
        files_ids = bsonimagelist.tomongo(fs)

    return True
