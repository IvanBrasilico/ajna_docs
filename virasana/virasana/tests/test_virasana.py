# Tescases for virasana.app.py
import unittest

from virasana.app import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        assert b'AJNA' in rv.data

    def test_list(self):
        rv = self.app.get('/list_files')
        assert b'AJNA' in rv.data
        # TODO: insert file and test return on list
