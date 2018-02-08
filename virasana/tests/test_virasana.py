# Tescases for padma.py
import json
import os
import unittest
from io import BytesIO

from virasana.virasanaapp import app

TEST_BSON = os.path.join(os.path.dirname(
    __file__), '..', '..', 'image_aq', 'tests', 'testlistvirasana.bson')


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_upload(self):
        bson = open(TEST_BSON, 'rb').read()
        data = {}
        data['file'] = (BytesIO(bson), 'testlist.bson')
        rv = self.app.post(
            '/uploadbson', content_type='multipart/form-data', data=data)
        test_dict = json.loads(rv.data.decode())
        print(test_dict)
        assert test_dict.get('success') is not None
        assert test_dict.get('success') is True