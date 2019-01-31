from datetime import timedelta

from flask import (Flask, flash, g, redirect, render_template, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, current_user, login_required, login_user)

import forms
import models


def create_app():
    models.initialize()
    app = Flask(__name__)
    app.secret_key = 'opu98wrwerworus.fmaouwerk,svlasnfweoru'
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @app.before_request
    def before_request():
        """connect to database before each request"""
        g.db = models.DATABASE
        g.db.connect()
        g.user = current_user

    @app.after_request
    def after_request(response):
        g.db.close()
        return response

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return models.User.get(models.User.id == user_id)
        except models.DoesNotExist:
            return None

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = forms.RegisterForm()
        if form.validate_on_submit():
            models.User.create_user(
                username=form.username.data,
                password=form.password.data
            )
            flash('congrats you are registered', category='success')
            return redirect(url_for('index'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = forms.LoginForm()
        if form.validate_on_submit():
            try:
                user = models.User.get(
                    models.User.username == form.username.data)
            except models.DoesNotExist:
                flash('oops that email or password does not match our records',
                      category='error')
            else:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash('you are logged in', category='success')
                    return redirect(url_for('index'))
                else:
                    flash(flash(
                        'oops that email or password does not match our'
                        'records',
                        category='error'))
        return render_template('login.html', form=form)

    @app.route('/add/entry', methods=['GET', 'POST'])
    @login_required
    def entry():
        count = 0
        form = forms.EntryForm()
        if form.validate_on_submit():

            models.Entry.create_entry(
                user=g.user._get_current_object(),
                title=form.title.data,
                date=form.date.data,
                time_spent=timedelta(seconds=float(form.time_spent.data)),
                knowledge_gained=form.knowledge_gained.data,
                resources=form.resources_to_remember.data,
            )

            if form.tag.data:
                tags = form.tag.data.split(',')
                for tag in tags:
                    models.Tag.create_tags(
                        name=tag
                    )
                    taggs = models.Tag.select().order_by(models.Tag.id.desc()).get()
                    models.JournalTags.insert(tag=taggs).execute()

            journal = models.Entry.select().order_by(models.Entry.id.desc()).get()
            models.JournalTags.insert(entry=journal).execute()
            import pdb;
            pdb.set_trace()

            flash('journal entry published', category='success')
            return redirect(url_for('index'))
        return render_template('new.html', form=form)

    @app.route('/edit/entry')
    def edit():
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
