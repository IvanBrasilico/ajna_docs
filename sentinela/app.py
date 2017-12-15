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

from flask import (abort, Flask, flash, redirect, render_template, request,
                   url_for)
from flask_bootstrap import Bootstrap
# from flask_cors import CORS
from flask_login import login_required, LoginManager, login_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from werkzeug.utils import secure_filename

from sentinela.models.models import (Base, BaseOrigem, BaseOriginal, MySession,
                                     ParametroRisco, ValorParametro, Visao)
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
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
users_repository = {'ajna': 'ajna'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('senha')
        registeredUser = users_repository.get(username)
        if registeredUser is not None and registeredUser == password:
            print('Logged in..')
            login_user(registeredUser)
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('index.html')


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


@app.route('/valores_parametro/<parametro_id>')
@login_required
def valores_parametro(parametro_id):
    valores = []
    paramrisco = session.query(ParametroRisco).filter(
        ParametroRisco.id == parametro_id
    ).first()
    if paramrisco:
        valores = paramrisco.valores
    return render_template('valores.html', valores=valores)


@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
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
@login_required
def list_files():
    """Lista arquivos csv disponíveis para trabalhar
    """
    lista_arquivos = [file for file in
                      os.listdir(UPLOAD_FOLDER) if allowed_file(file)]
    bases = session.query(BaseOriginal).all()
    return render_template('risco.html', lista_arquivos=lista_arquivos,
                           bases=bases)


@app.route('/importa')
@login_required
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
            return redirect(url_for('risco', baseid=baseid))
        except Exception as err:
            erro = err.__cause__
    return redirect(url_for('list_files', erro=erro))


@app.route('/risco', methods=['POST', 'GET'])
@app.route('/aplica_risco')
@login_required
def risco():
    lista_arquivos = []
    baseid = request.args.get('baseid', '0')
    padraoid = request.args.get('padraoid')
    visaoid = request.args.get('visaoid')
    path = request.args.get('filename')
    parametros_ativos = request.args.get('parametros_ativos')
    if parametros_ativos:
        parametros_ativos = parametros_ativos.split(',')
    try:
        for ano in os.listdir(os.path.join(CSV_FOLDER, baseid)):
            for mesdia in os.listdir(os.path.join(CSV_FOLDER, baseid, ano)):
                lista_arquivos.append(ano + '/' + mesdia)
    except FileNotFoundError:
        pass
    bases = session.query(BaseOrigem).all()
    padroes = session.query(BaseOriginal).all()
    visoes = session.query(Visao).all()
    parametros = []
    if padraoid:
        padrao = session.query(BaseOriginal).filter(
            BaseOriginal.id == padraoid
        ).first()
        if padrao:
            parametros = padrao.parametros
    if not path:
        return render_template('bases.html',
                               lista_arquivos=lista_arquivos,
                               bases=bases,
                               padroes=padroes,
                               visoes=visoes,
                               baseid=baseid,
                               padraoid=padraoid,
                               visaoid=visaoid,
                               parametros=parametros,
                               parametros_ativos=parametros_ativos)
    # if path aplica_risco
    gerente = GerenteRisco()
    opadrao = session.query(BaseOriginal).filter(
        BaseOriginal.id == padraoid).first()
    base_csv = os.path.join(CSV_FOLDER, baseid, path)
    gerente.set_base(opadrao)
    avisao = session.query(Visao).filter(
        Visao.id == visaoid).first()
    lista_risco = gerente.aplica_juncao(avisao, path=base_csv, filtrar=True,
                                        parametros_ativos=parametros_ativos)
    static_path = app.config.get('STATIC_FOLDER', 'static')
    csv_salvo = os.path.join(APP_PATH, static_path, 'baixar.csv')
    try:
        os.remove(csv_salvo)
    except IOError:
        pass
    with open(csv_salvo, 'w', encoding=ENCODE, newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(lista_risco)
    return render_template('bases.html',
                           lista_arquivos=lista_arquivos,
                           bases=bases,
                           padroes=padroes,
                           visoes=visoes,
                           baseid=baseid,
                           padraoid=padraoid,
                           visaoid=visaoid,
                           parametros=parametros,
                           parametros_ativos=parametros_ativos,
                           filename=path,
                           csv_salvo=os.path.basename(csv_salvo),
                           lista_risco=lista_risco)


@app.route('/edita_risco', methods=['POST', 'GET'])
@login_required
def edita_risco():
    padraoid = request.args.get('padraoid')
    padroes = session.query(BaseOriginal).all()
    parametros = []
    if padraoid:
        padrao = session.query(BaseOriginal).filter(
            BaseOriginal.id == padraoid
        ).first()
        if padrao:
            parametros = padrao.parametros
    id_parametro = request.args.get('id_parametro')
    valores = []
    if id_parametro:
        valor = session.query(ParametroRisco).filter(
            ParametroRisco.id == id_parametro
        ).first()
        if valor:
            valores = valor.valores
    return render_template('editarisco.html',
                           padraoid=padraoid,
                           padroes=padroes,
                           id_parametro=id_parametro,
                           parametros=parametros,
                           valores=valores)


@app.route('/aplica_risco2')
def aplica_risco2():
    baseid = request.args.get('base')
    visaoid = request.args.get('visao')
    path = request.args.get('filename')
    gerente = GerenteRisco()
    bases = session.query(BaseOriginal).all()
    visoes = session.query(Visao).all()
    abase = session.query(BaseOriginal).filter(
        BaseOriginal.id == baseid).first()
    base_csv = os.path.join(CSV_FOLDER, path)
    gerente.set_base(abase)
    avisao = session.query(Visao).filter(
        Visao.id == visaoid).first()
    lista_risco = gerente.aplica_juncao(avisao, path=base_csv, filtrar=True)
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
    return render_template('bases-adauto.html',
                           bases=bases,
                           baseid=baseid,
                           filename=path,
                           visoes=visoes,
                           csv_salvo=os.path.basename(csv_salvo),
                           lista_risco=lista_risco)


@app.route('/exclui_parametro')
def exclui_parametro():
    padraoid = request.args.get('padraoid')
    riscoid = request.args.get('riscoid')
    session.query(ParametroRisco).filter(
        ParametroRisco.id == riscoid).delete()
    session.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid))


@app.route('/adiciona_parametro')
def adiciona_parametro():
    padraoid = request.args.get('padraoid')
    risco_novo = request.args.get('risco_novo')
    risco = ParametroRisco(risco_novo)
    risco.base_id = padraoid
    session.add(risco)
    session.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid))


@app.route('/adiciona_valor')
def adiciona_valor():
    padraoid = request.args.get('padraoid')
    novo_valor = request.args.get('novo_valor')
    tipo_filtro = request.args.get('filtro')
    riscoid = request.args.get('riscoid')
    valor = ValorParametro(novo_valor, tipo_filtro)
    valor.risco_id = riscoid
    session.add(valor)
    session.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            id_parametro=riscoid))


@app.route('/exclui_valor')
def exclui_valor():
    padraoid = request.args.get('padraoid')
    riscoid = request.args.get('riscoid')
    valorid = request.args.get('valorid')
    session.query(ValorParametro).filter(
        ValorParametro.id == valorid).delete()
    session.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            id_parametro=riscoid))


@nav.navigation()
def mynavbar():
    return Navbar(
        'AJNA - Módulo Sentinela',
        View('Home', 'index'),
        View('Importar Bases', 'list_files'),
        View('Aplica Risco', 'risco'),
        View('Edita Riscos', 'edita_risco'),
    )


nav.init_app(app)


app.config['DEBUG'] = os.environ.get('DEBUG', 'None') == '1'
app.secret_key = 'sk'

if __name__ == '__main__':
    app.run()
