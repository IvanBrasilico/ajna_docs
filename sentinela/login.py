# from flask import Response, abort, redirect, render_template, request,url_for
# from flask_login import LoginManager, login_user
# Abaixo, importação circular, caso métodos de login forem ficar neste arquivo,
# código do app terá que ser chamado por arquivo raiz
# from sentinela.app import app

"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password, users_repository.next_index())
        users_repository.save_user(new_user)
        return Response('Registered Successfully')
    else:
        return render_template('index.html')


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@login_manager.user_loader
def load_user(userid):
    return users_repository.get(userid)
"""
