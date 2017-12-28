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
from urllib.parse import urljoin, urlparse

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from flask_bootstrap import Bootstrap
# from flask_cors import CORS
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from sentinela.conf import (ALLOWED_EXTENSIONS, APP_PATH, CSV_DOWNLOAD,
                            CSV_FOLDER, SECRET, UPLOAD_FOLDER)
from sentinela.models.models import (Base, BaseOrigem, DBUser, DePara,
                                     MySession, PadraoRisco, ParametroRisco,
                                     ValorParametro, Visao)
from sentinela.utils.csv_handlers import (sanitizar, sch_processing,
                                          unicode_sanitizar)
from sentinela.utils.gerente_base import Filtro, GerenteBase
from sentinela.utils.gerente_risco import ENCODE, GerenteRisco, tmpdir

mysession = MySession(Base)
dbsession = mysession.session
engine = mysession.engine

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

app = Flask(__name__, static_url_path='/static')
# CORS(app)
csrf = CSRFProtect(app)
Bootstrap(app)
nav = Nav()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(UserMixin):
    user_database = DBUser

    def __init__(self, id):
        self.id = id
        self.name = str(id)

    @classmethod
    def get(cls, username, password=None):
        dbuser = cls.user_database.get(dbsession, username, password)
        if dbuser:
            return User(dbuser.username)
        return None


def authenticate(username, password):
    user_entry = User.get(username, password)
    return user_entry


@login_manager.user_loader
def load_user(userid):
    user_entry = User.get(userid)
    return user_entry


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('senha')
        registered_user = authenticate(username, password)
        if registered_user is not None:
            print('Logged in..')
            login_user(registered_user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
        else:
            return abort(401)
    else:
        return render_template('index.html', form=request.form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    next = request.args.get('next')
    if not is_safe_url(next):
        next = None
    return redirect(next or url_for('index'))


def allowed_file(filename):
    """Check allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list_files')
@login_required
def list_files():
    """Lista arquivos csv disponíveis para trabalhar
    """
    lista_arquivos = sorted([file for file in
                             os.listdir(UPLOAD_FOLDER) if allowed_file(file)])
    bases = dbsession.query(PadraoRisco).order_by(PadraoRisco.nome).all()
    return render_template('importa_base.html', lista_arquivos=lista_arquivos,
                           bases=bases)


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
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('list_files'))
    return render_template('importa_base.html')


@app.route('/importa')
@login_required
def importa():
    erro = ''
    baseid = request.args.get('base')
    filename = request.args.get('filename')
    data = request.args.get('data')
    if not data:
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


@login_required
@app.route('/valores_parametro/<parametro_id>')
def valores_parametro(parametro_id):
    valores = []
    paramrisco = dbsession.query(ParametroRisco).filter(
        ParametroRisco.id == parametro_id
    ).first()
    if paramrisco:
        valores = paramrisco.valores
    return render_template('bases.html', valores=valores)


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
    bases = dbsession.query(BaseOrigem).order_by(BaseOrigem.nome).all()
    padroes = dbsession.query(PadraoRisco).order_by(PadraoRisco.nome).all()
    visoes = dbsession.query(Visao).order_by(Visao.nome).all()
    parametros = []
    if padraoid:
        padrao = dbsession.query(PadraoRisco).filter(
            PadraoRisco.id == padraoid
        ).first()
        if padrao:
            parametros = padrao.parametros
    parametro_id = request.args.get('parametroid')
    valores = []
    paramrisco = dbsession.query(ParametroRisco).filter(
        ParametroRisco.id == parametro_id
    ).first()
    if paramrisco:
        valores = paramrisco.valores
    if not path:
        return render_template('aplica_risco.html',
                               lista_arquivos=lista_arquivos,
                               bases=bases,
                               padroes=padroes,
                               visoes=visoes,
                               baseid=baseid,
                               valores=valores,
                               padraoid=padraoid,
                               visaoid=visaoid,
                               parametros=parametros,
                               parametros_ativos=parametros_ativos)
    # if path aplica_risco
    gerente = GerenteRisco()
    opadrao = dbsession.query(PadraoRisco).filter(
        PadraoRisco.id == padraoid).first()
    base_csv = os.path.join(CSV_FOLDER, baseid, path)
    gerente.set_base(opadrao)
    avisao = dbsession.query(Visao).filter(
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
    return render_template('aplica_risco.html',
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
    padroes = dbsession.query(PadraoRisco).order_by(PadraoRisco.nome).all()
    parametros = []
    if padraoid:
        padrao = dbsession.query(PadraoRisco).filter(
            PadraoRisco.id == padraoid
        ).first()
        if padrao:
            parametros = padrao.parametros
    riscoid = request.args.get('riscoid')
    valores = []
    if riscoid:
        valor = dbsession.query(ParametroRisco).filter(
            ParametroRisco.id == riscoid
        ).first()
        if valor:
            valores = valor.valores
    headers = dbsession.query(DePara).filter(
        DePara.base_id == padraoid
    ).all()
    if not headers:
        gerente = GerenteRisco()
        headers = gerente.import_named_csv(
            'sentinela/tests/BTP.csv', tolist=True)
    return render_template('edita_risco.html',
                           padraoid=padraoid,
                           padroes=padroes,
                           riscoid=riscoid,
                           parametros=parametros,
                           lista_autocomplete=headers,
                           valores=valores)


@app.route('/importa_csv/<padraoid>/<riscoid>', methods=['POST', 'GET'])
@login_required
def importa_csv(padraoid, riscoid):
    if request.method == 'POST':
        if 'csv' not in request.files:
            flash('No file part')
            return redirect(request.url)
        csvf = request.files['csv']
        print('FILE***', csvf.filename)
        if csvf.filename == '':
            flash('No selected file')
            return redirect(request.url)
        risco = None
        if riscoid:
            risco = dbsession.query(ParametroRisco).filter(
                ParametroRisco.id == riscoid).first()
        if risco is None:
            flash('Não foi selecionado parametro de risco')
            return redirect(request.url)
        if csvf and '.' in csvf.filename and \
                csvf.filename.rsplit('.', 1)[1].lower() == 'csv':
            # filename = secure_filename(csvf.filename)
            csvf.save(os.path.join(tmpdir, risco.nome_campo + '.csv'))
            print(csvf.filename)
            gerente = GerenteRisco()
            gerente.parametros_fromcsv(risco.nome_campo, session=dbsession)
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            riscoid=riscoid))


@app.route('/exporta_csv', methods=['POST', 'GET'])
@login_required
def exporta_csv():
    padraoid = request.args.get('padraoid')
    riscoid = request.args.get('riscoid')
    gerente = GerenteRisco()
    gerente.parametro_tocsv(riscoid, path=CSV_DOWNLOAD, dbsession=dbsession)
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            riscoid=riscoid))


@app.route('/exclui_parametro')
def exclui_parametro():
    padraoid = request.args.get('padraoid')
    riscoid = request.args.get('riscoid')
    dbsession.query(ParametroRisco).filter(
        ParametroRisco.id == riscoid).delete()
    dbsession.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid))


@app.route('/adiciona_parametro')
def adiciona_parametro():
    padraoid = request.args.get('padraoid')
    risco_novo = request.args.get('risco_novo')
    sanitizado = sanitizar(risco_novo, norm_function=unicode_sanitizar)
    risco = ParametroRisco(sanitizado)
    risco.base_id = padraoid
    dbsession.add(risco)
    dbsession.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid))


@app.route('/adiciona_valor')
def adiciona_valor():
    padraoid = request.args.get('padraoid')
    novo_valor = request.args.get('novo_valor')
    tipo_filtro = request.args.get('filtro')
    valor = sanitizar(novo_valor, norm_function=unicode_sanitizar)
    filtro = sanitizar(tipo_filtro, norm_function=unicode_sanitizar)
    riscoid = request.args.get('riscoid')
    valor = ValorParametro(valor, filtro)
    valor.risco_id = riscoid
    dbsession.add(valor)
    dbsession.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            riscoid=riscoid))


@app.route('/exclui_valor')
def exclui_valor():
    padraoid = request.args.get('padraoid')
    riscoid = request.args.get('riscoid')
    valorid = request.args.get('valorid')
    dbsession.query(ValorParametro).filter(
        ValorParametro.id == valorid).delete()
    dbsession.commit()
    return redirect(url_for('edita_risco', padraoid=padraoid,
                            riscoid=riscoid))


@app.route('/edita_depara')
@login_required
def edita_depara():
    baseid = request.args.get('baseid')
    bases = dbsession.query(BaseOrigem).all()
    titulos = []
    if baseid:
        base = dbsession.query(BaseOrigem).filter(
            BaseOrigem.id == baseid
        ).first()
        if base:
            titulos = base.deparas
    return render_template('muda_titulos.html', bases=bases,
                           baseid=baseid,
                           titulos=titulos)


@app.route('/adiciona_depara')
def adiciona_depara():
    baseid = request.args.get('baseid')
    titulo_antigo = request.args.get('antigo')
    titulo_novo = request.args.get('novo')
    if baseid:
        base = dbsession.query(BaseOrigem).filter(
            BaseOrigem.id == baseid
        ).first()
    depara = DePara(titulo_antigo, titulo_novo, base)
    dbsession.add(depara)
    dbsession.commit()
    return redirect(url_for('edita_depara', baseid=baseid))


@app.route('/exclui_depara')
def exclui_depara():
    baseid = request.args.get('baseid')
    tituloid = request.args.get('tituloid')
    dbsession.query(DePara).filter(
        DePara.id == tituloid).delete()
    dbsession.commit()
    return redirect(url_for('edita_depara', baseid=baseid))


@app.route('/navega_bases')
def navega_bases():
    selected_module = request.args.get('selected_module')
    selected_model = request.args.get('selected_model')
    selected_field = request.args.get('selected_field')
    filters = session.get('filters', [])
    gerente = GerenteBase()
    list_modulos = gerente.list_modulos
    list_models = []
    list_fields = []
    if selected_module:
        gerente.set_module(selected_module)
        list_models = gerente.list_models
        if selected_model:
            list_fields = gerente.dict_models[selected_model]['campos']
    return render_template('navega_bases.html',
                           selected_module=selected_module,
                           selected_model=selected_model,
                           selected_field=selected_field,
                           filters=filters,
                           list_modulos=list_modulos,
                           list_models=list_models,
                           list_fields=list_fields)


@app.route('/adiciona_filtro')
def adiciona_filtro():
    selected_module = request.args.get('selected_module')
    selected_model = request.args.get('selected_model')
    selected_field = request.args.get('selected_field')
    filters = session.get('filters', [])
    tipo_filtro = request.args.get('filtro')
    valor = request.args.get('valor')
    valor = sanitizar(valor, norm_function=unicode_sanitizar)
    afilter = Filtro(selected_field, tipo_filtro, valor)
    filters.append(afilter)
    session['filters'] = filters
    return redirect(url_for('navega_bases',
                            selected_module=selected_module,
                            selected_model=selected_model,
                            selected_field=selected_field,
                            filters=filters))


@app.route('/exclui_filtro')
def exclui_filtro():
    selected_module = request.args.get('selected_module')
    selected_model = request.args.get('selected_model')
    selected_field = request.args.get('selected_field')
    filters = session.get('filters', [])
    index = request.args.get('index')
    if filters:
        filters.pop(int(index))
    session['filters'] = filters
    return redirect(url_for('navega_bases',
                            selected_module=selected_module,
                            selected_model=selected_model,
                            selected_field=selected_field,
                            filters=filters))


@app.route('/consulta_bases_executar')
def consulta_bases_executar():
    selected_module = request.args.get('selected_module')
    selected_model = request.args.get('selected_model')
    selected_field = request.args.get('selected_field')
    filters = session.get('filters', [])
    gerente = GerenteBase()
    gerente.set_module(selected_module)
    dados = gerente.filtra(selected_model, filters)
    list_modulos = gerente.list_modulos
    list_models = []
    list_fields = []
    if selected_module:
        gerente.set_module(selected_module)
        list_models = gerente.list_models
        if selected_model:
            list_fields = gerente.dict_models[selected_model]['campos']
    # TODO: See how to make redirect passing data to consulta_bases on server
    return render_template('navega_bases.html',
                           selected_module=selected_module,
                           selected_model=selected_model,
                           selected_field=selected_field,
                           filters=filters,
                           list_modulos=list_modulos,
                           list_models=list_models,
                           list_fields=list_fields,
                           dados=dados)


@nav.navigation()
def mynavbar():
    items = [View('Home', 'index'),
             View('Importar Bases', 'list_files'),
             View('Aplicar Risco', 'risco'),
             View('Editar Riscos', 'edita_risco'),
             View('Editar Titulos', 'edita_depara'),
             View('Navega Bases', 'navega_bases')]
    if current_user.is_authenticated:
        items.append(View('Sair', 'logout'))
    return Navbar(
        'AJNA - Módulo Sentinela', *items)


nav.init_app(app)
app.config['DEBUG'] = os.environ.get('DEBUG', 'None') == '1'
if app.config['DEBUG'] is True:
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = SECRET
app.config['SECRET_KEY'] = SECRET
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
