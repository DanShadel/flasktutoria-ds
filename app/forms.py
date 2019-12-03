from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class URLForm(FlaskForm):
    input_url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Go!')