from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import (
                                DataRequired, ValidationError, Email,
                                EqualTo, Length, InputRequired
                                )

from models import User


def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exits')


class Register(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            username_exists
           ])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('confirm', message='Passwords must match')

        ])

    confirm = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired()
        ])