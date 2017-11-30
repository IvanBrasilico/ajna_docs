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
import csv
import datetime
import logging
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
# from flask_cors import CORS
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from werkzeug.utils import secure_filename

from sentinela.models.models import Base, BaseOriginal, MySession, Tabela
from sentinela.utils.csv_handlers import sch_processing
from sentinela.utils.gerente_risco import ENCODE, GerenteRisco

mysession = MySession(Base)
session = mysession.session
engine = mysession.engine

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

app = Flask(__name__, static_url_path='/static')
# CORS(app)
Bootstrap(app)
nav = Nav()

APP_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_PATH, 'files')
CSV_FOLDER = os.path.join(APP_PATH, 'CSV')
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'zip'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """Função simplificada para upload do arquivo de uma extração
    """
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
    bases = session.query(BaseOriginal).all()
    return render_template('risco.html', lista_arquivos=lista_arquivos,
                           bases=bases)


@app.route('/importa')
def importa():
    erro = ''
    baseid = request.args.get('base')
    filename = request.args.get('filename')
    data = request.args.get('data')
    if data is None:
        data = datetime.date.today().strftime('%Y%m%d')
    if baseid is not None and filename is not None:
        dest_path = os.path.join(CSV_FOLDER, baseid, data[:4], data[4:])
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        try:
            sch_processing(os.path.join(UPLOAD_FOLDER,
                                        secure_filename(filename)),
                           dest_path=dest_path)
            return redirect(url_for('risco'))
        except Exception as err:
            erro = err.__cause__
    return redirect(url_for('list_files', erro=erro))


@app.route('/risco')
def risco():
    lista_arquivos = []
    for base in os.listdir(CSV_FOLDER):
        for ano in os.listdir(os.path.join(CSV_FOLDER, base)):
            for mesdia in os.listdir(os.path.join(CSV_FOLDER, base, ano)):
                lista_arquivos.append(base + '/' + ano + '/' + mesdia)
    bases = session.query(BaseOriginal).all()
    return render_template('bases.html',
                           lista_arquivos=lista_arquivos,
                           bases=bases)


@app.route('/aplica_risco')
def aplica_risco():
    baseid = request.args.get('base')
    path = request.args.get('filename')
    gerente = GerenteRisco()
    bases = session.query(BaseOriginal).all()
    abase = session.query(BaseOriginal).filter(
        BaseOriginal.id == baseid).first()
    base_csv = os.path.join(CSV_FOLDER, path)
    gerente.set_base(abase)
    tabela = session.query(Tabela).filter(
        Tabela.id == 1).first()
    lista_risco = gerente.aplica_juncao(tabela, path=base_csv, filtrar=True,
                                        campos=['Conhecimento',
                                                'Container',
                                                'CPFCNPJConsignatario',
                                                'DescricaoMercadoria',
                                                'IdentificacaoEmbarcador'
                                                ])
    print(lista_risco)
    static_path = app.config.get('STATIC_FOLDER', 'static')
    csv_salvo = os.path.join(APP_PATH, static_path, 'baixar.csv')
    try:
        os.remove(csv_salvo)
    except IOError:
        pass
    with open(csv_salvo, 'w', encoding=ENCODE) as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(lista_risco)
    return render_template('bases.html',
                           bases=bases,
                           baseid=baseid,
                           filename=path,
                           csv_salvo=os.path.basename(csv_salvo),
                           lista_risco=lista_risco)


@nav.navigation()
def mynavbar():
    return Navbar(
        'AJNA - Módulo Sentinela',
        View('Home', 'index'),
        View('Importação', 'list_files'),
        View('Risco', 'risco'),
    )


nav.init_app(app)

app.config['DEBUG'] = os.environ.get('DEBUG', 'None') == '1'

if __name__ == '__main__':
    app.run()
