from flask_wtf import FlaskForm
from wtforms import FormField, IntegerField, PasswordField, StringField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, EqualTo, Length, Optional, ValidationError)

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


class TagForm(FlaskForm):
    name = StringField(
        "Tags",
        validators=[
            Optional()
        ],
        render_kw={
            'placeholder': 'separate tags by commas'
        }
    )


class EntryForm(FlaskForm):
    title = StringField(
        'Title',

    )
    date = DateField(
        'DatePicker'



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
        ],
        render_kw={
            'placeholder': 'separate resources by new line'
        }

    )

    name = FormField(TagForm)


class EditForm(FlaskForm):
    title = StringField(
        'Title',

    )
    date = DateField(
        'date',

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

    name = FormField(TagForm)
