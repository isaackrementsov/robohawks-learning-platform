import os
import uuid

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email


class LoginForm(FlaskForm):

    emailOrUsername = TextField('EmailAddressOrUsername', [Required()])
    password = PasswordField('Password', [Required()])


class CreateForm(FlaskForm):

    email = TextField('Email', [Required(), Email()])
    username = TextField('Username', [Required()])
    first_name = TextField('FirstName', [Required()])
    last_name = TextField('LastName', [Required()])
    password = PasswordField('Password', [Required()])
    admin = BooleanField('Admin')
