# Tescases for padma.py
import datetime
import json
import os
import unittest
import pytest
from io import BytesIO

from celery import states
import gridfs
from pymongo import MongoClient

from ajna_img_functions.models.bsonimage import BsonImage, BsonImageList
from virasana.app import app, BROKER, BACKEND, celery


TEST_BSON = os.path.join(os.path.dirname(
    __file__), 'test.bson')
TEST_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_FOLDER = os.path.join(TEST_PATH)

files_ids = None


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': BROKER,
        'result_backend': BACKEND
    }


@pytest.fixture(scope='session')
def celery_parameters():
    return {
        'task_cls': celery.task_cls,
        'strict_typing': False,
    }


class FlaskTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def init_worker(self, celery_worker):
        self.worker = celery_worker

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self._bsonimage = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp1.jpg'),
            chave='virasana1',
            origem=0,
            data=datetime.datetime.utcnow()
        )
        self._bsonimage2 = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp2.jpg'),
            chave='virasana2',
            origem=1,
            data=datetime.datetime.utcnow()
        )
        bsonimagelist = BsonImageList()
        bsonimagelist.addBsonImage(self._bsonimage)
        bsonimagelist.addBsonImage(self._bsonimage2)
        bsonimagelist.tofile(TEST_BSON)
        self._db = MongoClient().test
        self._fs = gridfs.GridFS(self._db)

    def tearDown(self):
        os.remove(TEST_BSON)
        files = self._fs.find({'metadata.chave': 'virasana1'})
        for file in files:
            self._fs.delete(file._id)
        files = self._fs.find({'metadata.chave': 'virasana2'})
        for file in files:
            self._fs.delete(file._id)

    def test_upload(self):
        bson = open(TEST_BSON, 'rb').read()
        data = {}
        data['file'] = (BytesIO(bson), 'test.bson')
        rv = self.app.post(
            '/uploadbson', content_type='multipart/form-data', data=data)
        test_dict = json.loads(rv.data.decode())
        print(test_dict)
        assert test_dict.get('state') is not None
        assert test_dict.get('state') == states.SUCCESS
        assert self._fs.find_one({'metadata.chave': 'virasana1'}) is not None
        assert self._fs.find_one({'metadata.chave': 'virasana2'}) is not None
