from flask import (Flask, render_template,
                   flash, redirect, url_for, g)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         login_required, logout_user, current_user)

import forms
from datetime import datetime, time, timedelta

import models


def create_app():
    app = Flask(__name__)
    app.secret_key = 'opu98wrwerworus.fmaouwerk,svlasnfweoru'
    login_manager = LoginManager ()

    login_manager.init_app (app)
    DEBUG = True
    PORT = 8000
    HOST = '0.0.0.0'

    @app.before_request
    def before_request():
        """connect to database before each request"""
        g.db = models.DATABASE
        g.db.connect ()
        g.user = current_user

    @app.after_request
    def after_request(response):
        g.db.close ()
        return response

    @app.route('/register', methods=['POST'])
    def register():
        form = forms.Register()
        if form.validate_on_submit():
            models.User.create_users(
                username=form.username.data,
                password=form.password.data
                )
            flash('congrats you are registered', category='success')
            redirect(url_for('index'))
        return render_template('register.html', form=form)

    @app.route('/')
    def hello_world():
        return 'Hello World!'
    return app


if __name__ == '__main__':
    models.initialize()
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
