import datetime
import unittest
import os

from image_aq.models.bsonimage import BsonImage

IMG_FOLDER = 'padma/tests/'


class TestModel(unittest.TestCase):
    def setUp(self):
        self.mongosession = None

    def tearDown(self):
        pass

    def test1_bson(self):
        self._bson = BsonImage(
            filename = os.path.join(IMG_FOLDER, 'stamp1.jpg'),
            chave = 'MSKU123',
            origem = 0,
            data = datetime.datetime.now()

        )


if __name__ == '__main__':
    unittest.main()
