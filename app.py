from flask import (Flask, render_template,
                   flash, redirect, url_for, g)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         login_required, logout_user, current_user)

import forms
from datetime import datetime, time, timedelta

from models import initialize
from models import User


def create_app():
    app = Flask(__name__)

    DEBUG = True
    PORT = 8000
    HOST = '0.0.0.0'

    @app.route('/register')
    def register():
        form = forms.Register()
        if form.validate_on_submit():
            User.create_users(
                username=form.username.data,
                password=form.password.data
                )
            flash('congrats you are registered', category='success')
            redirect(url_for('index'))
        render_template('register.html', form=form)


    @app.route('/')
    def hello_world():
        return 'Hello World!'
    return app


if __name__ == '__main__':
    initialize()
    app = create_app()
    app.run(host='0.0.0.0',port=8000, debug=True)
