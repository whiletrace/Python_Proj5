from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import (
    DataRequired, EqualTo, Length, ValidationError
)

import models


def username_exists(form, field):
    if models.User.select().where(
            models.User.username == field.data).exists():
        raise ValidationError('User already exits')


class RegisterForm(FlaskForm):
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


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired()
        ]
    )


class EntryForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )
    date = DateField(
        'DatePicker',
        format='%Y-%m-%d',


    )
    time_spent = IntegerField(
        "time spent",
        validators=[
            DataRequired()
        ]
    )
    knowledge = TextAreaField(
        "What I Learned",
        validators=[
            DataRequired()
        ]
    )
    resources = TextAreaField(
        "Resources To Remember",
        validators=[
            DataRequired()
        ]
    )
    tag = StringField(
        "create tags",
        validators=[
            DataRequired()
        ]
    )

# class TagForm(FlaskForm):
# tag = StringField()
