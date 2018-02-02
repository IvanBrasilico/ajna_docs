# Tescases for models/vazios/vazios.py
import os
import unittest

from PIL import Image

from models.vazios.vazios import VazioModel

VAZIO_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')
CHEIO_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')


class TestModel(unittest.TestCase):
    def setUp(self):
        self.vazio = Image.open(VAZIO_IMAGE)
        self.cheio = Image.open(CHEIO_IMAGE)
        self.model = VazioModel()

    def tearDown(self):
        pass

    def test_histogram(self):
        hist = self.model.hist(self.vazio)
        assert hist is not None

    def test_vazio_image(self):
        preds = self.model.vaziooucheio(image=self.vazio)
        print(preds)
        assert preds[0][0] > 0.5

    def test_vazio_file(self):
        preds = self.model.vaziooucheio(file=VAZIO_IMAGE)
        print(preds)
        assert preds[0][0] > 0.5

    def test_cheio_image(self):
        preds = self.model.vaziooucheio(image=self.cheio)
        print(preds)
        assert preds[0][1] > 0.5

    def test_cheio_file(self):
        preds = self.model.vaziooucheio(file=CHEIO_IMAGE)
        print(preds)
        assert preds[0][1] > 0.5

    def test_descritivo(self):
        desc = self.model.vaziooucheiodescritivo(image=self.cheio)
        assert "NÃO" in desc
        desc = self.model.vaziooucheiodescritivo(image=self.vazio)
        assert "NÃO" not in desc
 
