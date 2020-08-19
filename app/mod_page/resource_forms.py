from app.utils import FileUtils

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, HiddenField
from wtforms.validators import Required


class CreateAndUpdateResourceForm(FlaskForm):

    link = TextField('Link')
    file = FileField()
    sequence = HiddenField('Sequence', [Required()])

    def save_file(self):
        return FileUtils.save_file(self.file, 'resources')
