from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import (
    DataRequired, EqualTo, Length, ValidationError, Regexp
)

import models


def username_exists(form, field):
    if models.User.select().where(
            models.User.username == field.data).exists():
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


class Login(FlaskForm):
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


class Entry(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )
    date = DateField(
        'Date',
        validators=[
            Regexp(
                r'^(\d{2}\/\d{2}\/\d{4})',
                message='date should be entered in the format MM/DD/YYYY'
            ),
            DataRequired()
        ],
        format='%m:%d:%Y'
    )
    time_spent = IntegerField(
        "time spent",
        validators=[
            DataRequired()
        ]
    )
    knowledge_gained = TextAreaField(
        "What I Learned",
        validators=[
            DataRequired()
        ]
    )
    resources_to_remember = TextAreaField(
        "Resources To Remember",
        validators=[
            DataRequired()
        ]
    )


class Tag(FlaskForm):
    tag = StringField()
