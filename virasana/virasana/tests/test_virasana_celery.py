# Tescases for padma.py
import datetime
# import json
import os
import unittest
from io import BytesIO

import gridfs
import pytest
from ajna_img_functions.models.bsonimage import BsonImage, BsonImageList
# from celery import states
from pymongo import MongoClient

from virasana.app import BACKEND, BROKER, app, celery

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


class FlaskCeleryBsonTestCase(unittest.TestCase):
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
        # os.remove(TEST_BSON)
        files = self._fs.find({'metadata.chave': 'virasana1'})
        for file in files:
            self._fs.delete(file._id)
        files = self._fs.find({'metadata.chave': 'virasana2'})
        for file in files:
            self._fs.delete(file._id)


class FlaskCeleryBsonTestCase1(FlaskCeleryBsonTestCase):
    def test_apiupload(self):
        bson = open(TEST_BSON, 'rb').read()
        data = {}
        data['file'] = (BytesIO(bson), 'test.bson')
        rv = self.app.post(
            '/uploadbson', content_type='multipart/form-data', data=data)
        print(rv.data)
        assert rv.data is not None


"""
        rv = self.app.post(
            '/api/uploadbson', content_type='multipart/form-data', data=data)
        print(rv.data)
        assert rv.data is not None
        test_dict = json.loads(rv.data.decode())
        print(test_dict)
        assert test_dict.get('state') is not None
        assert test_dict.get('state') == states.SUCCESS
        assert self._fs.find_one({'metadata.chave': 'virasana1'}) is not None
        assert self._fs.find_one({'metadata.chave': 'virasana2'}) is not None

"""
"""
# TODO: more than one Celery test not working... See whats going on.
class FlaskCeleryBsonTestCase2(FlaskCeleryBsonTestCase):
    def test_upload(self):
        bson = open(TEST_BSON, 'rb').read()
        data = {}
        data['file'] = (BytesIO(bson), 'test.bson')
        rv = self.app.post(
            '/api/uploadbson', content_type='multipart/form-data', data=data)
        # TODO: when raspadir_progress is Done,
        #  wait for response and test here!
        assert rv.data is not None
"""
