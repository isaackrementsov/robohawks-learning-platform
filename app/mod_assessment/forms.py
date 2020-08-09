from flask_wtf import FlaskForm

from wtforms import TextField, TextAreaField
from wtforms.validators import Required


class CreateAndUpdateForm(FlaskForm):

    name = TextField('Name', [Required()])
    text_content = TextAreaField('TextContent', render_kw={'rows': 5, 'cols': 5})
