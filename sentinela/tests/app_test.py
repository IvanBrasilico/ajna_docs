"""Tests and documents use of the Web UI
Any client must make this type of request to Web UI
Made from Flask testing docs
http://flask.pocoo.org/docs/0.12/testing/
"""
import unittest

import sentinela.app as app


class FlaskTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.arquivo = ''
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_not_found(self):
        rv = self.app.get('/non_ecsiste')
        assert b'404 Not Found' in rv.data

    def test_home(self):
        rv = self.app.get('/')
        print(rv)
        assert b'AJNA' in rv.data

    def test_risco(self):
        rv = self.app.get('/risco')
        print(rv)
        assert b'input type="file"' in rv.data

    def test_listfiles(self):
        rv = self.app.get('/list_files')
        print(rv)
        assert b'input type="file"' in rv.data

    def test_bases(self):
        rv = self.app.get('/base/teste.txt')
        print(rv)
        assert b'teste.txt' in rv.data
        assert b'<select name="base"' in rv.data

    def test_aplica_risco(self):
        rv = self.app.get('/aplica_risco?filename=tests.zip&base=1')
        print(rv)
        assert b'tests.zip' in rv.data
        assert b'<select name="base"' in rv.data

    def _post(self, url, data):
        rv = self.app.post(url, data=data, follow_redirects=True)
        print(rv)
