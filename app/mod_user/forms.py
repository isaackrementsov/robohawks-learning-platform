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


class UpdateForm(FlaskForm):

    email = TextField('Email', [Required(), Email()])
    username = TextField('Username', [Required()])
    first_name = TextField('FirstName', [Required()])
    last_name = TextField('LastName', [Required()])
    password = PasswordField('Password', [Required()])
    avatar = FileField()

    # TODO: Implement mime checking
    def save_avatar(self):
        return FileUtils.save_file(self.avatar, '/avatars')
