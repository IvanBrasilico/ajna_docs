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

        if self.http_server is not None:
            from webtest import TestApp
            self.app = TestApp(self.http_server)
        else:
            app.app.testing = True
            app.app.config['WTF_CSRF_ENABLED'] = False
            self.app = app.app.test_client()
        rv = self.login('ajna', 'ajna')
        assert rv is not None

    def tearDown(self):
        rv = self.logout()
        assert rv is not None

    def login(self, username, senha):
        if self.http_server is not None:
            # First, get the CSRF Token
            response = self.app.get('/login')
            self.csrf_token = str(response.html.find_all(
                attrs={'name': 'csrf_token'})[0])
            begin = self.csrf_token.find('value="') + 7
            end = self.csrf_token.find('"/>')
            self.csrf_token = self.csrf_token[begin: end]
            response = self.app.post('/login',
                                     params=dict(
                                         username=username,
                                         senha=senha,
                                         csrf_token=self.csrf_token)
                                     )
            return response
        else:
            return self.app.post('/login', data=dict(
                username=username,
                senha=senha
            ), follow_redirects=True)

    def logout(self):
        if self.http_server is not None:
            return self.app.get('/logout',
                                params=dict(csrf_token=self.csrf_token))
        else:
            return self.app.get('/logout', follow_redirects=True)

    def test_not_found(self):
        if self.http_server is None:
            rv = self.app.get('/non_ecsiste')
            assert b'404 Not Found' in rv.data

    def data(self, rv):
        if self.http_server is not None:
            return str(rv.html).encode('utf_8')
        return rv.data

    def test_home(self):
        if self.http_server is not None:
            rv = self.app.get('/',
                              params=dict(csrf_token=self.csrf_token))
        else:
            rv = self.app.get('/')
        data = self.data(rv)
        assert b'AJNA' in data

    def test_upload_file(self):
        if self.http_server is not None:
            rv = self.app.get('/upload_file',
                              params=dict(csrf_token=self.csrf_token))
        else:
            rv = self.app.get('/upload_file')
        data = self.data(rv)
        assert b'="file"' in data
        rv = self._post('/upload_file', data={'file': ''}, follow_redirects=False)
        self.assertTrue(rv.status_code == 302)
        data2 = self.data(rv)
        assert b'Redirecting..' in data2

    def test_listfiles(self):
        if self.http_server is not None:
            rv = self.app.get('/list_files',
                              params=dict(csrf_token=self.csrf_token))
        else:
            rv = self.app.get('/list_files')
        data = self.data(rv)
        assert b'AJNA' in data

    def test_importa(self):
        if self.http_server is not None:
            rv = self.app.get('/importa',
                              params=dict(csrf_token=self.csrf_token))
        else:
            rv = self.app.get('/importa')
        data = self.data(rv)
        assert b'Redirecting...' in data

    def test_risco(self):
        if self.http_server is not None:
            rv = self.app.get('/risco?base=1',
                              params=dict(csrf_token=self.csrf_token))
        else:
            rv = self.app.get('/risco?base=1')
        data = self.data(rv)
        # dt = rv.get_data(as_text=True)
        assert b'Lista de Riscos' in data
        rp = self._post('/risco', data={'file': 'file1'})
        data2 = self.data(rp)
        assert b'Escolha Base' in data2

    def _post(self, url, data, follow_redirects=True):
        if self.http_server is not None:
            data['csrf_token'] = self.csrf_token
            rv = self.app.post(url, params=data)
        else:
            rv = self.app.post(url, data=data, follow_redirects=follow_redirects)
        return rv

    """
    def test_valores(self):
        # valores = [1, 2, 3]
        rv = self.app.get('/valores_parametro/{valores}')
        data = self.data(rv)
        # dt = rv.get_data(as_text=True)
        assert b'Lista de Valores' in data
    """


"""

    def test_risco2(self):
        rv = self.app.get('/edita_risco?padraoid=1')
        data = self.data(rv)
        assert b'AJNA' in data

    # Gerar arquivos para poder fazer este teste automático
    def test_aplica_risco(self):
        rv = self.app.get('/aplica_risco?filename=../tests&base=1')
        print(rv)
        # assert b'tests.zip' in rv.data
        assert b'<select name="base"' in rv.data
"""
