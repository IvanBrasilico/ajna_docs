import datetime
import unittest
import os
import gridfs
from pymongo import MongoClient
from image_aq.models.bsonimage import BsonImage


TEST_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_FOLDER = os.path.join(TEST_PATH, '..', '..', 'padma/tests/')

IMG_FOLDER = '/home/ivan/pybr/AJNA_MOD/padma/tests/'

class TestModel(unittest.TestCase):
    def setUp(self):
        self._bsonimage = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp1.jpg'),
            chave='MSKU123',
            origem=0,
            data=datetime.datetime.now()

        )
        self._db = MongoClient().test
        self._fs = gridfs.GridFS(self._db)

    def tearDown(self):
        pass

    def test1_bjson(self):
        self._bsonimage.tobson()

    def test2_savefile(self):
        self._bsonimage.tofile(os.path.join(TEST_PATH, 'test.bjson'))

    def test3_savemongo(self):
        self._bsonimage.tomongo(self._fs)


if __name__ == '__main__':
    unittest.main()
