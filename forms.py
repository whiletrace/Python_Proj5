from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import (DataRequired, EqualTo, Length, ValidationError)

import models


def username_exists(form, field):
    if models.User.select ().where (
            models.User.username == field.data).exists ():
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


class Login (FlaskForm):
    username = StringField (
        "Username",
        validators=[
            DataRequired ()
        ]
    )
    password = PasswordField (
        validators=[
            DataRequired ()
        ]
    )
