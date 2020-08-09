from app.utils import FileUtils

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, TextAreaField, HiddenField, BooleanField
from wtforms.validators import Required

class CreateAndUpdateForm(FlaskForm):

    name = TextField('Name', [Required()])
    description = TextAreaField('Description', [Required()])
    icon = HiddenField('Icon', [Required()])
    micro = BooleanField('Micro', [Required()])
