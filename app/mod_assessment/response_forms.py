from app.utils import FileUtils

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import TextField, HiddenField, TextAreaField, NumberField, BooleanField
from wtforms.validators import Required


class CreateResponseForm(FlaskForm):

    letter = HiddenField('Letter')
    correct = BooleanField('Correct')
    text = TextAreaField('Text') # Make the size depend on question type
    file = FileField()


    def save_file(self):
        return FileUtils.save_file(self.file, 'responses')


class UpdateResponseForm(CreateResponseForm):

    score = NumberField('Score')
    feedback = TextField('Feedback')


class CreateAndUpdateAnswerForm(CreateResponseForm):

    strict = BooleanField('Strict', [Required()])
    sequence = HiddenField('Sequence', [Required()])
