from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_integrum.models import User



#Registreringsformuläret med inbyggda valideringar genom wtforms
class RegistrationForm(FlaskForm):
    username = StringField("Användarnamn",
                           [DataRequired(),
                            Length(min=3, 
                            max=20, 
                            message=
                            "Användarnamnet måste vara mellan 3-20 tecken!")])

    email = StringField("Email",
                        validators=[DataRequired(),
                        Email(message="Skriv in en giltig email adress!")])

    password = PasswordField("Lösenord (Minst 6 tecken långt)", 
                        validators=[DataRequired(),
                        Length(min=6, 
                        max=100, 
                        message=
                        "Lösenordet måste vara minst 6 tecken långt!")])

    confirm_password = PasswordField("Bekräfta lösenord",
                        validators=[DataRequired(), 
                        EqualTo("password", 
                        message="Lösenorden matchar inte!")])

    submit = SubmitField("Registrera")


    def validate_username(self, username):
        #Kollar om användarnamnet som anges redan finns i databasen
        user = User.query.filter_by(username=username.data).first()
        #Om användaren redan finns, skriv felmeddelande.
        if user:
            raise ValidationError("Användarnamnet är upptaget!")

    def validate_email(self, email):
        #Kollar om emailen som anges redan finns i databasen
        user = User.query.filter_by(email=email.data).first()
        #Om emailen redan finns, skriv felmeddelande. Annars gå vidare
        if user:
            raise ValidationError("Emailen finns redan registrerad!")
        


#Login formuläret med inbyggda valideringar genom wtforms
class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), 
                        Email(message="Ogiltig email adress")])

    password = PasswordField("Lösenord",
                             validators=[DataRequired()])

    #Frågar om användaren om hen vill spara sitt lösenord
    remember = BooleanField("Kom ihåg mig")

    submit = SubmitField("Logga in")



#Formuläret under profilsidan där man kan uppdatera användarnamn + email
class UpdateAccountForm(FlaskForm):
    username = StringField("Nytt användarnamn",
                           [DataRequired(), 
                           Length(min=3,
                            max=20, 
                            message=
                            "Användarnamnet måste vara mellan 3-20 tecken!")])

    email = StringField("Ny email",
                        validators=[DataRequired(),
                        Email(message=
                        "Skriv in en giltig email adress!")])

    picture = FileField("Uppdatera profilbild",
                        validators=[FileAllowed(["jpg", "png"], 
                        message=
                        "Ogiltigt filformat,"\
                        "använd filformat 'jpg' eller 'png'")])

    submit = SubmitField("Uppdatera")

    def validate_username(self, username):
        #Kollar att anvgivet användarnamn inte 
        #är samma som användaren redan har
        if username.data != current_user.username:
            #Kollar om användarnamnet som anges redan finns i databasen
            user = User.query.filter_by(username=username.data).first()
            #Om användaren redan finns, skriv ut felmeddelande. 
            #Annars gå vidare
            if user:
                raise ValidationError("Användarnamnet är upptaget!")

    def validate_email(self, email):
        #Kollar att anvgiven email inte 
        #är samma som användaren redan har
        if email.data != current_user.email:
            #Kollar om emailen som anges redan finns i databasen
            user = User.query.filter_by(email=email.data).first()
            #Om emailen redan finns, skriv ut felmeddelande.
            if user:
                raise ValidationError("Emailen finns redan registrerad!")



#Formuläret där man anger sin email 
#för att återställa sitt lösenord 
#kontrollerar om emailen finns registrerad
class RequestResetForm(FlaskForm):
    email = StringField("Ange Email",
                        validators=[DataRequired(), 
                        Email(message=
                        "Skriv in en giltig email adress!")])
    submit = SubmitField("Validera Email")

    #Validera att email som anges finns i databasen
    def validate_email(self, email):
        #Kollar om emailen som anges finns i databasen
        user = User.query.filter_by(email=email.data).first()
        #Om emailen inte finns, skriv ut felmeddelande. Annars gå vidare
        if user is None:
            raise ValidationError("Det finns inget konto med angiven email!")



#Formuläret där man anger sitt nya lösenord
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Lösenord", 
                        validators=[DataRequired(), 
                        Length(min=6, 
                        max=100,
                        message=
                        "Lösenordet måste vara minst 6 tecken långt!")])

    confirm_password = PasswordField("Bekräfta lösenord",
                        validators=[DataRequired(), 
                        EqualTo("password", 
                        message=
                        "Lösenorden matchar inte!")])
    
    submit = SubmitField("Återställ Lösenord")