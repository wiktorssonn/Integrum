from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from flask import flash
from flask_login import current_user



class PostAssignment(FlaskForm):
    assignment = StringField('Uppgift:', validators=[DataRequired(message="Du måste ange ett uppgiftsnamn!")])
    description = TextAreaField('Beskrivning:', validators=[DataRequired(message="Du måste skriva något!")])
    submit = SubmitField('Lägg till')


class PostItem(FlaskForm):
    Title = StringField('Titel', validators=[DataRequired(message="Du måste ange en titel!")])
    course = TextAreaField('Kurs:', validators=[DataRequired(message="Du måste ange vilken kurs boken används i!")])
    Contact = StringField('Kontakt: ', validators=[DataRequired(message="Du måste ange email eller telefonnummer!")])
    price = StringField('Pris: ', validators=[DataRequired(message="Du måste ange ett pris för boken!")])
    submit = SubmitField('Lägg till')