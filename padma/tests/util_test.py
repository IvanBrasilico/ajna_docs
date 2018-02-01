#Tescases for utils.py
import os
import unittest

from PIL import Image

from app.utils import base64_decode_image, base64_encode_image, prepare_image

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_CHANS = 3
IMAGE_DTYPE = 'float32'

TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class TestModel(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base64_encode_decode_image(self):
        image = Image.open(TEST_IMAGE)
        image = prepare_image(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        image = image.copy(order='C')
        encoded = base64_encode_image(image)
        decoded = base64_decode_image(encoded, IMAGE_DTYPE,
                                      (1, IMAGE_HEIGHT, IMAGE_WIDTH,
                                       IMAGE_CHANS))
        assert image.any() == decoded.any()
