from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from flask import flash
from flask_login import current_user



class PostAssignment(FlaskForm):
    title = StringField('Uppgift:', validators=[DataRequired(message="Du måste ange ett uppgiftsnamn!")])
    description = TextAreaField('Beskrivning:', validators=[DataRequired(message="Du måste skriva något!")])
    submit = SubmitField('Skicka')