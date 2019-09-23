# Tescases for virasana.app.py
import json
import unittest

import ajna_commons.flask.user as user_ajna
from ajna_commons.flask import api_login
from ajna_commons.flask.conf import MONGODB_URI
from flask import Flask
from pymongo import MongoClient


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['SERVER_NAME'] = 'test.api'
        self.app = app
        app.secret_key = 'DUMMY'
        app.testing = True
        self.client = app.test_client()
        self.db = MongoClient(host=MONGODB_URI).unit_test
        user_ajna.DBUser.dbsession = self.db
        user_ajna.DBUser.add('ajna', 'ajna')
        conn = MongoClient(host=MONGODB_URI)
        api_login.configure(app)

    def tearDown(self):
        # self.db.drop_collection('users')
        pass

    def app_test(self, method, url, pjson):
        if method == 'POST':
            return self.client.post(
                url,
                data=json.dumps(pjson),
                content_type='application/json')
        else:
            return self.client.get(url)

    def _case(self, method='POST',
              url='api/login',
              pjson=None,
              status_code=200,
              msg=''):
        try:
            r = self.app_test(method, url, pjson)
            print(r.status_code)
            print(r.data)
            print(r.json)
            assert r.status_code == status_code
            if r.json and msg:
                assert r.json.get('msg') == msg
        except json.JSONDecodeError as err:
            print(err)
            assert False

    def test_json_requerido(self):
        self._case(status_code=400, msg='JSON requerido')

    def test_usuario_obrigatorio(self):
        self._case(pjson={'dummy': 'dummy'},
                   status_code=400,
                   msg='Parametro username requerido')

    def test_password_obrigatorio(self):
        self._case(pjson={'username': 'ivan'},
                   status_code=400,
                   msg='Parametro password requerido')

    def test_login_ok(self):
        self._case(pjson={'username': 'ivan', 'password': 'ivan'},
                   status_code=401)

    def test_login_invalido(self):
        self._case(pjson={'username': 'ajna', 'password': 'ajna'},
                   status_code=200)

    def test_unauthorized(self):
        rv = self.client.get('api/test')
        assert rv.status_code == 401

    def test_login_access_test(self):
        rv = self.client.post(
            'api/login',
            data=json.dumps({'username': 'ajna', 'password': 'ajna'}),
            content_type='application/json')
        token = rv.json.get('access_token')
        headers = {'Authorization': 'Bearer ' + token}
        rv = self.client.get('api/test', headers=headers)
        assert rv.status_code == 200


    def test_logout_unauthorized(self):
        rv = self.client.post(
            'api/login',
            data=json.dumps({'username': 'ajna', 'password': 'ajna'}),
            content_type='application/json')
        token = rv.json.get('access_token')
        headers = {'Authorization': 'Bearer ' + token}
        rv = self.client.get('api/test', headers=headers)
        assert rv.status_code == 200
        rv = self.client.delete('api/logout', headers=headers)
        print(rv)
        assert rv.json.get('msg') == 'Logout efetuado'
        rv = self.client.get('api/test', headers=headers)
        assert rv.status_code == 401
