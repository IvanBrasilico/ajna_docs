# -*- coding: utf-8 -*-
"""
Módulo Sentinela - AJNA
=======================

Interface do Usuário - WEB
--------------------------

Módulo responsável por gerenciar bases de dados importadas/acessadas pelo AJNA,
administrando estas e as cruzando com parâmetros de risco.

Serve para a administração, pré-tratamento e visualização dos dados importados,
assim como para acompanhamento de registros de log e detecção de problemas nas
conexões internas.

Adicionalmente, permite o merge entre bases a aplicação de filtros /
parâmetros de risco.
"""
import logging
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
# from flask_cors import CORS
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from werkzeug.utils import secure_filename

from sentinela.models.models import Base, BaseOriginal, MySession
from sentinela.utils.csv_handlers import sch_processing
from sentinela.utils.gerente_risco import GerenteRisco

mysession = MySession(Base)
session = mysession.session
engine = mysession.engine

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

app = Flask(__name__, static_url_path='/static')
# CORS(app)
Bootstrap(app)
nav = Nav()

path = os.path.dirname(os.path.abspath(__file__))
containers_file = 'conteiners.csv'
UPLOAD_FOLDER = os.path.join(path, 'files')
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'zip'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
memory_log = []
memory_report = {}


def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/risco', methods=['GET', 'POST'])
def upload_file():
    """Função simplificada para upload do arquivo CSV de extração
    Arquivo precisa de uma coluna chamada Conteiner e uma coluna chamada Lacre
    """
    print('risco')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print('FILE***', file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('list_files'))
    return render_template('risco.html')


@app.route('/list_files')
def list_files():
    """Lista arquivos csv disponíveis para trabalhar
    """
    lista_arquivos = [file for file in
                      os.listdir(UPLOAD_FOLDER) if allowed_file(file)]
    return render_template('risco.html', lista_arquivos=lista_arquivos)


@app.route('/base/<filename>')
def base(filename):
    bases = session.query(BaseOriginal).all()
    return render_template('bases.html',
                           bases=bases,
                           filename=filename)


@app.route('/aplica_risco')
def aplica_risco():
    baseid = request.args.get('base')
    filename = request.args.get('filename')
    gerente = GerenteRisco()
    bases = session.query(BaseOriginal).all()
    abase = session.query(BaseOriginal).filter(
        BaseOriginal.id == baseid).first()
    filenames = sch_processing(os.path.join(UPLOAD_FOLDER,
                                            secure_filename(filename)))
    gerente.set_base(abase)
    # Preferencialmente vai tentar processar o arquivo de conhecimentos
    # Se não houver, pega o primeiro da lista mesmo
    # Depois será utilizado o aplica_juncao no lugar desta "gambiarra"
    ind = 0
    for cont, afile in enumerate(filenames):
        if afile[0].find('Conhecimento'):
            ind = cont
            break
    lista_risco = gerente.aplica_risco(arquivo=filenames[ind][0])
    return render_template('bases.html',
                           bases=bases,
                           baseid=baseid,
                           filename=filename,
                           lista_risco=lista_risco)


@nav.navigation()
def mynavbar():
    return Navbar(
        'AJNA - Módulo Sentinela',
        View('Home', 'index'),
        View('Risco', 'upload_file'),
    )


nav.init_app(app)

app.config['DEBUG'] = os.environ.get('DEBUG', 'None') == '1'

if __name__ == '__main__':
    app.run()
