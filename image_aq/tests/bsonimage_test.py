import datetime
import os
import unittest

import bson
import gridfs
from pymongo import MongoClient

from image_aq.models.bsonimage import BsonImage, BsonImageList

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_FOLDER = os.path.join(TEST_PATH, '..', '..', 'padma/tests/')


class TestModel(unittest.TestCase):
    def setUp(self):
        self._bsonimage = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp1.jpg'),
            chave='MSKU123',
            origem=0,
            data=datetime.datetime.utcnow()
        )
        self._bsonimage2 = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp2.jpg'),
            chave='MSKU1234',
            origem=1,
            data=datetime.datetime.utcnow()
        )
        self._bsonimagelist = BsonImageList()
        self._bsonimagelist.addBsonImage(self._bsonimage)
        self._bsonimagelist.addBsonImage(self._bsonimage2)
        self._db = MongoClient().test
        self._fs = gridfs.GridFS(self._db)

    def tearDown(self):
        pass

    def test1_bjson(self):
        mybson = self._bsonimage.tobson
        mydict = bson.BSON.decode(mybson)
        assert mydict.get('metadata').get(
            'chave') == self._bsonimage._metadata.get('chave')

    def test1_savefile(self):
        self._bsonimage.tofile(os.path.join(TEST_PATH, 'test.bjson'))
        self._bsonimage.tofile(os.path.join(
            TEST_PATH, 'test.bjson.zip'), zipped=True)

    def test2_loadfile(self):
        bsonimage = BsonImage.fromfile(os.path.join(TEST_PATH, 'test.bjson'))
        assert bsonimage._metadata.get(
            'chave') == self._bsonimage._metadata.get('chave')
        bsonimage = BsonImage.fromfile(os.path.join(
            TEST_PATH, 'test.bjson.zip'), zipped=True)
        assert bsonimage._metadata.get(
            'chave') == self._bsonimage._metadata.get('chave')


    def test6_savefilelist(self):
        self._bsonimagelist.tofile(os.path.join(TEST_PATH, 'testlist.bjson'))

    def test7_loadfilelist(self):
        bsonimagelist = BsonImageList.fromfile(
            os.path.join(TEST_PATH, 'testlist.bjson'))
        assert bsonimagelist.tolist[0]._metadata.get(
            'chave') == self._bsonimage._metadata.get('chave')
        assert bsonimagelist.tolist[1]._metadata.get(
            'chave') == self._bsonimage2._metadata.get('chave')
"""
MONGO TESTS commented to not run in CI

    def test4_savemongo(self):
        file_id = self._bsonimage.tomongo(self._fs)
        print('File id', file_id)
        assert file_id is not None

    def test5_loadmongo(self):
        file_id = self._bsonimage.tomongo(self._fs)
        bsonimage = BsonImage.frommongo(file_id, self._fs)
        assert bsonimage._metadata.get(
            'chave') == self._bsonimage._metadata.get('chave')

    def test8_savemongolist(self):
        files_ids = self._bsonimagelist.tomongo(self._fs)
        print('File ids', files_ids)
        assert files_ids is not None

    def test5_loadmongolist(self):
        files_ids = self._bsonimagelist.tomongo(self._fs)
        bsonimagelist = BsonImageList.frommongo(files_ids, self._fs)
        assert bsonimagelist.tolist[0]._metadata.get(
            'chave') == self._bsonimage._metadata.get('chave')

"""

if __name__ == '__main__':
    unittest.main()
