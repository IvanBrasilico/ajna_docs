# Tescases for utils.py
import json
import os
import requests
import unittest
from io import BytesIO

from PIL import Image

from app.padma import app, classify_process

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_CHANS = 3
IMAGE_DTYPE = 'float32'

TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_prediction(self):
        image = open(TEST_IMAGE, "rb").read()
        data = {}
        data['image'] = (BytesIO(image), 'image')
        rv = self.app.post(
            '/predict', content_type='multipart/form-data', data=data)
        test_dict = json.loads(rv.data.decode())
        assert test_dict.get('success') is not None
        assert test_dict.get('success') is True
        assert test_dict.get('predictions')[0].get('label') == 'beagle'
        assert b'beagle' in rv.data
