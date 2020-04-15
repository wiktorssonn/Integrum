# Importerar FlaskForm som har färdiga formulärfunktioner!
from flask_wtf import FlaskForm
#Vilka filer som får laddas upp som profilbild
from flask_wtf.file import FileField, FileAllowed
#Importerar aktuell användare som är inloggad
from flask_login import current_user
# Importerar Olika sorters field för olika typer av fält
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# Importerar olika validators så att rätt information fylls i
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#Importerar User från models.py
from flask_integrum.models import User


#Registreringsformuläret med inbyggda valideringar genom wtforms
class RegistrationForm(FlaskForm):
    username = StringField("Användarnamn",
                           [DataRequired(), Length(min=3, max=20, message="Användarnamnet måste vara mellan 3-20 tecken!")])

    email = StringField("Email",
                        validators=[DataRequired(), Email(message="Skriv in en giltig email adress!")])

    password = PasswordField("Lösenord", 
                        validators=[DataRequired(), Length(min=6, max=100, message="Lösenordet måste vara minst 6 tecken långt!")])

    confirm_password = PasswordField("Bekräfta lösenord",
                        validators=[DataRequired(), EqualTo("password", message="Lösenorden matchar inte!")])

    submit = SubmitField("Registrera")


    def validate_username(self, username):
        #Kollar om användarnamnet som anges redan finns i databasen
        user = User.query.filter_by(username=username.data).first()
        #Om användaren redan finns, skriv ut felmeddelande. Annars gå vidare
        if user:
            raise ValidationError("Användarnamnet är upptaget!")

    def validate_email(self, email):
        #Kollar om emailen som anges redan finns i databasen
        user = User.query.filter_by(email=email.data).first()
        #Om emailen redan finns, skriv ut felmeddelande. Annars gå vidare
        if user:
            raise ValidationError("Emailen finns redan registrerad!")
        


#Login formuläret med inbyggda valideringar genom wtforms
class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email(message="Ogiltig email adress")])

    password = PasswordField("Lösenord",
                             validators=[DataRequired()])

    #Frågar om användaren om hen vill spara sitt lösenord
    remember = BooleanField("Kom ihåg mig")

    submit = SubmitField("Login")



class PostForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired(message="Du måste ange en titel!")])
    content = TextAreaField('Innehåll', validators=[DataRequired(message="Du måste skriva något!")])
    submit = SubmitField('Skicka')



class UpdateAccountForm(FlaskForm):
    username = StringField("Användarnamn",
                           [DataRequired(), Length(min=3, max=20, message="Användarnamnet måste vara mellan 3-20 tecken!")])

    email = StringField("Email",
                        validators=[DataRequired(), Email(message="Skriv in en giltig email adress!")])

    picture = FileField("Uppdatera profilbild", validators=[FileAllowed(["jpg", "png"], message="Ogiltigt filformat, använd filformat 'jpg' eller 'png'")])

    submit = SubmitField("Uppdatera")

    def validate_username(self, username):
        #Kollar att anvgivet användarnamn inte är samma som användaren redan har
        if username.data != current_user.username:
            #Kollar om användarnamnet som anges redan finns i databasen
            user = User.query.filter_by(username=username.data).first()
            #Om användaren redan finns, skriv ut felmeddelande. Annars gå vidare
            if user:
                raise ValidationError("Användarnamnet är upptaget!")

    def validate_email(self, email):
        #Kollar att anvgiven email inte är samma som användaren redan har
        if email.data != current_user.email:
            #Kollar om emailen som anges redan finns i databasen
            user = User.query.filter_by(email=email.data).first()
            #Om emailen redan finns, skriv ut felmeddelande. Annars gå vidare
            if user:
                raise ValidationError("Emailen finns redan registrerad!")
