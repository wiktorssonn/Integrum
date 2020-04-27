from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired(message="Du måste ange en titel!")])
    content = TextAreaField('Innehåll', validators=[DataRequired(message="Du måste skriva något!")])
    submit = SubmitField('Skicka')