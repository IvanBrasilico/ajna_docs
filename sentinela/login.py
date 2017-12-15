from flask_login import LoginManager, login_user
from flask import Response, abort, redirect, render_template, request, url_for




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
"""


class User():
    user_database = {'ivan': ('ivan', 'ivan')}

    def __init__(self, id):
        self.id = id
        self.name = 'user' + str(id)
        self.password = self.name + '_secret'

    def __repr__(self):
        return '%d/%s/%s' % (self.id, self.name, self.password)

    @classmethod
    def get(cls, id):
        return cls.user_database.get(id)


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@login_manager.user_loader
def load_user(userid):
    return users_repository.get(userid)
