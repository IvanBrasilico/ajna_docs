# Tescases for models/vazios/vazios.py
import os
import unittest

from PIL import Image

from keras.preprocessing.image import img_to_array
from models.bbox.bbox import NaiveModel, RetinaModel

IMAGE = os.path.join(os.path.dirname(__file__), 'stamp1.jpg')


class TestModel(unittest.TestCase):
    def setUp(self):
        self.image = img_to_array(Image.open(IMAGE))
        self.naive = NaiveModel()
        self.retina = RetinaModel()

    def tearDown(self):
        pass

    def test_naive(self):
        preds = self.naive.predict(self.image)
        print(preds)
        assert False

    def test_resnet(self):
        preds = self.retina.predict(self.image)
        print(preds)
        assert False


if __name__ == '__main__':
    unittest.main()
