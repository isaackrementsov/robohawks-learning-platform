from app.utils import FileUtils

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, TextAreaField
from wtforms.validators import Required


class CreateAndUpdateForm(FlaskForm):

    name = TextField('Name', [Required()])
    description = TextAreaField('Description', [Required()])
    cover = FileField('Cover', [Required()])

    def save_file(self):
        return FileUtils.save_file(self.file, 'responses')
