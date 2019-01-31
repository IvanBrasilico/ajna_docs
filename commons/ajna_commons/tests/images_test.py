import datetime
import os
import unittest

import gridfs
from pymongo import MongoClient

from ajna_commons.models.bsonimage import BsonImage
from ajna_commons.utils.images import get_imagens_recortadas

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_FOLDER = os.path.join(TEST_PATH)


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
        self._db = MongoClient().unit_test
        self._fs = gridfs.GridFS(self._db)
        self.file_id = self._bsonimage.tomongo(self._fs)
        self.file_id2 = self._bsonimage2.tomongo(self._fs)

    def tearDown(self):
        self._fs.delete(self.file_id)
        self._fs.delete(self.file_id2)

    def test_get_imagens_recortadas(self):
        self._db['fs.files'].update_one({'_id': self.file_id},
                                        {'$set':
                                         {'metadata.predictions':
                                          [{'bbox': [0, 0, 10, 10]}]
                                          }
                                         }
                                        )
        imagens = get_imagens_recortadas(self._db, self.file_id)
        assert imagens != []
        assert len(imagens) == 1
        self._db['fs.files'].update_one({'_id': self.file_id},
                                        {'$set':
                                         {'metadata.predictions':
                                          [{'bbox': [0, 0, 10, 10]},
                                           {'bbox': [0, 10, 10, 20]}]
                                          }
                                         }
                                        )
        imagens = get_imagens_recortadas(self._db, self.file_id)
        assert len(imagens) == 2

    def test_get_imagens_recortadas_sem_bbox(self):
        imagens = get_imagens_recortadas(self._db, self.file_id2)
        assert imagens == []


if __name__ == '__main__':
    unittest.main()
