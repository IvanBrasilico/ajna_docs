# Tescases for padma.py
import json
import os
import unittest
from io import BytesIO

from threading import Thread

from app.padma import app, classify_process

TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        t = Thread(target=classify_process, args=())
        t.daemon = True
        t.start()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_prediction_ResNet(self):
        image = open(TEST_IMAGE, "rb").read()
        data = {}
        data['image'] = (BytesIO(image), 'image')
        rv = self.app.post(
            '/predict?model=resnet', content_type='multipart/form-data', data=data)
        test_dict = json.loads(rv.data.decode())
        assert test_dict.get('success') is not None
        assert test_dict.get('success') is True
        assert test_dict.get('predictions')[0].get('label') == 'beagle'
        assert b'beagle' in rv.data

    def test_prediction_Vazios(self):
        image = open(TEST_IMAGE, "rb").read()
        data = {}
        data['image'] = (BytesIO(image), 'image')
        rv = self.app.post(
            '/predict?model=vazios', content_type='multipart/form-data', data=data)
        test_dict = json.loads(rv.data.decode())
        assert test_dict.get('success') is not None
        assert test_dict.get('success') is True
        assert test_dict.get('predictions') is not None
        assert b'"1"' in rv.data
