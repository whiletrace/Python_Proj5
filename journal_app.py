import datetime

from flask import (Flask, flash, g, redirect,
                   render_template, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, current_user,
                         login_required, login_user, logout_user)

import forms
import models

app = Flask(__name__)

app.secret_key = 'opu98wrwerworus.fmaouwerk,svlasnfweoru'

login_manager = LoginManager(app)

login_manager.init_app(app)

login_manager.login_view = 'login'


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('index'))


@app.route('/add/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form = forms.EntryForm()
    if form.validate_on_submit():

        models.Entry.create_entry(
            user=g.user._get_current_object(),
            title=form.title.data,
            date=(form.date.data.strftime('%m/%d/%Y')),
            time_spent=datetime.timedelta(seconds=float(form.time_spent.data)),
            knowledge=form.knowledge.data,
            resources=form.resources.data.splitlines()
        )
        journal_entry = models.Entry.get(title=form.title.data)

        if form.tag.data:
            tag_data = form.tag.data.split(',')
            tags = []
            for item in tag_data:
                tag = models.Tag.get_or_create_tags(
                    name=item
                )
                tags.append(tag)

            models.JournalTags.create_relations(journal_entry, tags)

        flash('journal entry published', category='success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/', methods=['GET'])
def index():
    all_entries = models.Entry.select()
    return render_template('index.html', all_entries=all_entries)


@app.route('/user', methods=['GET'])
@login_required
def user_entries():
    try:
        # need to get the current logged in user
        user = current_user
        # need to get current logged in user entries
        journal_entries = models.User.select().where(models.Entry.user == user.id)
        return render_template('user_stream.html', journal_entries=journal_entries)
    except ValueError:
        print('cant get this ')


@app.route('/entries/<int:entry_id>', methods=["GET"])
def entries(entry_id):
    # grab the id of the journal entry and pass that to the Url
    single_entry = models.Entry.select().where(models.Entry.id == entry_id).get()

    # import pdb ; pdb.set_trace()
    # query the and db and select the Entry that matches the id that is passed through the url
    # render and pass that to the details pg and then render the correct entry within the template
    return render_template('detail.html', single_entry=single_entry)


@app.route('/entries/edit/<int:entry_id>', methods=['GET', 'Post'])
def edit_entries(entry_id):
    entry_to_edit = models.Entry.select().where(models.Entry.id == entry_id).get()
    form = forms.EntryForm()
    form.title.data = entry_to_edit.title
    form.date.data = entry_to_edit.date
    form.time_spent.data = entry_to_edit.time_spent
    form.knowledge.data = entry_to_edit.knowledge
    form.resources.data = entry_to_edit.resources
    return render_template('edit.html', form=form, entry_to_edit=entry_to_edit)
    # need to get pass the entry id from detail pg
    # pass the entry id to the URL
    # store that entry in variable using a query to the User Model

    # populate the entry form with data from select query
    # upon the submit button update the contents of the entry
    # alert the user that the update has taken place
    # constraints = if owner of the Entry is not the current user do not allow edit

    pass


if __name__ == "__main__":
    models.initialize()
    models.User.create_user(
        username='trace',
        password='password'
    )
    models.User.create_user(
        username='uncle',
        password='password',
    )
    models.Entry.create_entry(
        user=1,
        title='a wonderful',
        date=datetime.datetime.now(),
        time_spent=datetime.timedelta(minutes=234),
        knowledge='I know things that only someone of my standing could know',
        resources='eggs and coffee\n lsd\n yayo'.splitlines()

    )
    models.Entry.create_entry(
        user=2,
        title='life and bounty ',
        date=datetime.datetime.now(),
        time_spent=datetime.timedelta(minutes=988),
        knowledge='yeah that first guy doesnt know squat',
        resources='''eggs and coffee\r lsd\r yayo'''.splitlines()
    )
    app.run(port=8000)