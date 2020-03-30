# Importerar FlaskForm som har färdiga formulärfunktioner
from flask_wtf import FlaskForm
# Importerar Olika sorters field för olika typer av fält
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Importerar olika validators så att rätt information fylls i
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Användarnamn",
                           validators=[DataRequired(), Length(min=3, max=20)])

    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Lösenord",
                             validators=[DataRequired()])

    confirm_password = PasswordField("Bekräfta lösenord",
                                     validators=[DataRequired(), EqualTo("Lösenord")])

    submit = SubmitField("Registrera")


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Lösenord",
                             validators=[DataRequired()])

    # Låter användaren vara inloggad en stund efter webbläsaren stängs
    remember = BooleanField("Kom ihåg mig")

    submit = SubmitField("Login")
