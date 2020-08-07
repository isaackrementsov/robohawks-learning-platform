from app.utils import FileUtils

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, SelectField, TextAreaField, NumberField, BooleanField
from wtforms.validators import Required


class UpdateForm(FlaskForm):

    text_content = TextAreaField('TextContent', render_kw={'rows': 5, 'cols': 5})
    sequence = HiddenField('Sequence', [Required()])
    all_required = BooleanField('AllRequired')
    file = FileField()

    def save_file(self):
        return FileUtils.save_file(self.file, 'resources')


class CreateForm(UpdateForm):

    type = SelectField('Type', [Required()], choices=[('multiple_choice', 'Multiple choice'), ('short_answer', 'Short answer'), ('long_answer', 'Long answer')])
    score_total = NumberField('ScoreTotal')
