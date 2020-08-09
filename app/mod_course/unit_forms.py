from flask_wtf import FlaskForm

from wtforms import TextField
from wtforms.validators import Required


class CreateAndUpdateForm(FlaskForm):

    name = TextField('Name', [Required()])
