import datetime

from flask import (Flask, flash, g, redirect,
                   render_template, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, current_user,
                         login_required, login_user, logout_user)
from flask_wtf.csrf import CSRFProtect

import dummy_data
import forms
import models

app = Flask(__name__)
CSRFProtect(app)
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
                flash(
                    'oops that email or password does not match our'
                    'records',
                    category='error')
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
    form1 = forms.TagForm()
    if form.validate_on_submit():

        models.Entry.create_entry(
            user=g.user._get_current_object(),
            title=form.title.data,
            date=form.date.data,
            time_spent=datetime.timedelta(minutes=float(form.time_spent.data)),
            knowledge=form.knowledge.data,
            resources=form.resources.data.splitlines()
        )
        journal_entry = models.Entry.get(title=form.title.data)

        if form1.validate_on_submit():
            tag_data = form1.name.data.split(',')
            tags = []
            for item in tag_data:
                tag = models.Tag.get_or_create_tags(
                    name=item
                )
                tags.append(tag)

            models.JournalTags.create_relations(journal_entry, tags)

        flash('journal entry published', category='success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form, form1=form1)


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
    entry_tags = (models.Tag.select().join(models.JournalTags).where(models.JournalTags.entry == single_entry)
                  .order_by(models.Tag.name))



    # query the and db and select the Entry that matches the id that is passed through the url
    # render and pass that to the details pg and then render the correct entry within the template
    return render_template('detail.html', single_entry=single_entry, entry_tags=entry_tags)


# pass the entry id to the URL
# need to get pass the entry id from detail pg
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entries(entry_id):
    # store value of query Entry with id that matches value passed
    # queries
    entry_to_edit = models.Entry.select().where(models.Entry.id == entry_id).get()
    entry_tags = (models.Tag.select().join(models.JournalTags).where(models.JournalTags.entry == entry_to_edit)
                  .order_by(models.Tag.name))

    import pdb;
    pdb.set_trace()
    all_tags = models.Tag.select()
    # variables

    tags = [tag.name for tag in entry_tags]
    parsed_tags = ','.join(tags)
    entry_owner = entry_to_edit.user
    form = forms.EditForm(obj=entry_to_edit)
    form1 = forms.TagForm(
        name=parsed_tags
    )
    # constraints = if owner of the Entry is not the current user do not allow edit
    if current_user == entry_owner:
        # populate the entry form with data from select query
        # upon the submit button update the contents of the entry

        if form.validate_on_submit():
            form.populate_obj(entry_to_edit)
            entry_to_edit.time_spent = datetime.timedelta(minutes=float(form.time_spent.data))
            entry_to_edit.date = datetime.date.strptime(form.date.data, "%Y-%m-%d")
            entry_to_edit.resources = form.resources.data.splitlines()
            models.Entry.save(entry_to_edit)

        if form1.validate_on_submit():
            # first convert form data into a list
            tag_data = form1.name.data.split(',')
            # iterate through unedited tags
            for tag_obj in entry_tags:
                # if the tag is not found in form data the relationship to the entry is broken
                if tag_obj.name not in tag_data:
                    # break relations is a class method performs delete query at the through table
                    models.JournalTags.break_relations(tag_obj, entry_to_edit)
            # iterate through the form tag list
            for item in tag_data:
                if item not in tags:
                    tag_data[:].remove(item)
                    tag = [models.Tag.get_or_create_tags(item)]
                    models.JournalTags.create_relations(entry_to_edit, tag)

            # alert the user that the update has taken place
            flash('hey we updated your entry', category='success')
            return redirect(url_for('index'))
    else:
        flash('you need to be the entries owner to edit this', category='error')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, form1=form1)


@app.route('/delete/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    entry_to_delete = models.Entry.select().where(models.Entry.id == entry_id).get()
    entry_owner = entry_to_delete.user
    if current_user == entry_owner:
        try:
            q = models.Entry.delete().where(models.Entry.id == entry_to_delete.id)
            q.execute()
            flash('your entry has been deleted', category='success')
            return redirect(url_for('index'))
        except models.DoesNotExist:
            return None
    else:
        flash("you must be the owner of this entry to be able to delete", category='error')
        return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()

    dummy_data.entry_1()
    dummy_data.entry_2()
    app.run(port=8000)
