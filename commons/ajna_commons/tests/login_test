# Tescases for virasana.app.py
import os
import unittest

import virasana.app as app
from ajna_commons.flask.login import DBUser


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.http_server = os.environ.get('HTTP_SERVER')
        if self.http_server is not None:
            from webtest import TestApp
            self.app = TestApp(self.http_server)
        else:
            app.app.testing = True
            app.app.config['WTF_CSRF_ENABLED'] = False
            self.app = app.app.test_client()
            DBUser.dbsession = None  # Bypass mongodb authentication

    def tearDown(self):
        rv = self.logout()
        assert rv is not None

    def login(self, username, senha, next_url=''):
        url = '/login'
        if next_url:
            url = url + '?next=' + next_url
        print(url)
        if self.http_server is not None:
            # First, get the CSRF Token
            response = self.app.get('/login')
            self.csrf_token = str(response.html.find_all(
                attrs={'name': 'csrf_token'})[0])
            begin = self.csrf_token.find('value="') + 7
            end = self.csrf_token.find('"/>')
            self.csrf_token = self.csrf_token[begin: end]
            response = self.app.post(url,
                                     params=dict(
                                         username=username,
                                         senha=senha,
                                         csrf_token=self.csrf_token)
                                     )
            return response
        else:
            return self.app.post(url, data=dict(
                username=username,
                senha=senha,
            ), follow_redirects=True)

    def logout(self):
        if self.http_server is not None:
            return self.app.get('/logout',
                                params=dict(csrf_token=self.csrf_token))
        else:
            return self.app.get('/logout', follow_redirects=True)

    def test_login_invalido(self):
        rv = self.login('none', 'error')
        print(rv)
        assert rv is not None
        assert b'401' in rv.data

    def test_next_invalido(self):
        pass
        """
        rv = self.login('ajna', 'ajna', 'www.google.com')
        print(rv)
        assert rv is not None
        assert b'400' in rv.data
        """

    def test_index(self):
        rv = self.login('ajna', 'ajna')
        assert rv is not None
        rv = self.app.get('/', follow_redirects=True)
        assert b'AJNA' in rv.data

    def test_upload_bson(self):
        self.login('ajna', 'ajna')
        rv = self.app.get('/uploadbson', follow_redirects=True)
        assert b'AJNA' in rv.data
        print(rv.data)

    def test_task_progress(self):
        self.login('ajna', 'ajna')
        rv = self.app.get('/api/task/123')
        assert b'state' in rv.data
        print(rv.data)

    def test_list(self):
        self.login('ajna', 'ajna')
        rv = self.app.get('/list_files')
        assert b'AJNA' in rv.data
        print(rv.data)
        # TODO: insert file and test return on list

    def test_file(self):
        self.login('ajna', 'ajna')
        # rv = self.app.get('/file/123')
        # assert b'AJNA' in rv.data
        # print(rv.data)

    def test_image(self):
        self.login('ajna', 'ajna')
        # rv = self.app.get('/image/123')
        # assert b'AJNA' in rv.data
        # print(rv.data)

    def test_files(self):
        self.login('ajna', 'ajna')
        rv = self.app.get('/files')
        assert b'AJNA' in rv.data
        print(rv.data)
