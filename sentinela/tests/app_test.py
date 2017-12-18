"""Tests and documents use of the Web UI
Any client must make this type of request to Web UI
Made from Flask testing docs
http://flask.pocoo.org/docs/0.12/testing/
"""
import os
import unittest

import sentinela.app as app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Ativar esta variável de ambiente na inicialização
        # do Servidor WEB para transformar em teste de integração
        self.http_server = os.environ.get('HTTP_SERVER')
        # TODO: Pesquisar método para testar mesmo com CSRF habilitado
        # https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
        app.app.config['WTF_CSRF_ENABLED'] = False

        if self.http_server is not None:
            from webtest import TestApp
            self.app = TestApp(self.http_server)
        else:
            app.app.testing = True
            self.app = app.app.test_client()
        rv = self.login('ajna', 'ajna')
        assert rv is not None

    def tearDown(self):
        rv = self.logout()
        assert rv is not None

    def login(self, username, senha):
        return self.app.post('/login', data=dict(
            username=username,
            senha=senha
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_not_found(self):
        if self.http_server is None:
            rv = self.app.get('/non_ecsiste')
            assert b'404 Not Found' in rv.data

    def data(self, rv):
        if self.http_server is not None:
            return rv.html
        return rv.data

    def test_home(self):
        rv = self.app.get('/')
        data = self.data(rv)
        assert b'AJNA' in data

    def test_upload_file(self):
        rv = self.app.get('/upload_file')
        data = self.data(rv)
        assert b'input type="file"' in data
        rp = self.app.post('/upload_file', data={'file': ''})
        self.assertTrue(rp.status_code == 302)
        data2 = self.data(rp)
        assert b'Redirecting...' in data2

    def test_listfiles(self):
        rv = self.app.get('/list_files')
        data = self.data(rv)
        assert b'input type="file"' in data

    def test_importa(self):
        rv = self.app.get('/importa')
        data = self.data(rv)
        assert b'Redirecting...' in data

    def test_risco(self):
        rv = self.app.get('/risco?base=1')
        data = self.data(rv)
        # dt = rv.get_data(as_text=True)
        assert b'Lista de Riscos' in data
        rp = self.app.post('/risco', data={'file': 'file1'})
        data2 = self.data(rp)
        assert b'Escolha Base' in data2

    def _post(self, url, data):
        rv = self.app.post(url, data=data, follow_redirects=True)
        print(rv)

    """def test_valores(self):
        # valores = [1, 2, 3]
        rv = self.app.get('/valores_parametro/{valores}')
        data = self.data(rv)
        # dt = rv.get_data(as_text=True)
        assert b'Lista de Valores' in data
    """

    def test_risco2(self):
        rv = self.app.get('/edita_risco?padraoid=1')
        data = self.data(rv)
        assert b'AJNA' in data


"""
    # Gerar arquivos para poder fazer este teste automático
    def test_aplica_risco(self):
        rv = self.app.get('/aplica_risco?filename=../tests&base=1')
        print(rv)
        # assert b'tests.zip' in rv.data
        assert b'<select name="base"' in rv.data
"""
