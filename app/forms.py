from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class URIForm(FlaskForm):
    uri = StringField('URI', validators=[DataRequired()])
    submit = SubmitField('Go!')