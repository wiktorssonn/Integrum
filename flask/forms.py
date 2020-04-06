# Importerar FlaskForm som har färdiga formulärfunktioner!
from flask_wtf import FlaskForm
# Importerar Olika sorters field för olika typer av fält
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Importerar olika validators så att rätt information fylls i
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#Importerar psyopg2 för att prata med databasen
import psycopg2


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

    #Kontrollerar att användarnamnet som angetts inte redan finns i databasen
    def validate_username(self, username):
        #Ansluter till databasen
        try:
            connection = psycopg2.connect(user = "aj8772",
                                    password = "z7zz9fgh",
                                    host = "pgserver.mah.se",
                                    database = "integrum_db")
            cursor = connection.cursor()
            print("Connected to database")
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            
        #Emailen som angetts i formuläret läggs i variabeln username
        username = username.data 
    
        #Hämtar alla användare från users table i databasen
        cursor.execute("select * from users")
        all_users = cursor.fetchall()
        
        #Kontrollerar om användarnamnet som angetts i formuläret redan finns i databasen
        name_in_use = False
        for user in all_users:
            if username.lower() == user[1].lower():
                name_in_use = True
        
        #Om användarnamnet redan finns, skriv ut felmeddelande
        if name_in_use == True:
            raise ValidationError("Användarnamnet är upptaget!")

        #Om emailen inte finns så går den vidare till register-routen och slutför skrivning till databasen


    #Kontrollerar att emailen som angetts inte redan finns i databasen
    def validate_email(self, email):
        #Ansluter till databasen
        try:
            connection = psycopg2.connect(user = "aj8772",
                                    password = "z7zz9fgh",
                                    host = "pgserver.mah.se",
                                    database = "integrum_db")
            cursor = connection.cursor()
            print("Connected to database")
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            
        #Emailen som angetts i formuläret läggs i variabeln email
        email = email.data 
    
        #Hämtar alla email från users table i databasen
        cursor.execute("select * from users")
        all_emails = cursor.fetchall()
        
        #Kontrollerar om emailen som angetts i formuläret redan finns i databasen
        email_in_use = False
        for mail in all_emails:
            if email.lower() == mail[2].lower():
                email_in_use = True
        
        #Om emailen redan finns, skriv ut felmeddelande
        if email_in_use == True:
            raise ValidationError("Denna mail finns redan registrerad!")

        #Om emailen inte finns så går den vidare till register-routen och slutför skrivning till databasen
        


#Login formuläret med inbyggda valideringar genom wtforms
class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Lösenord",
                             validators=[DataRequired()])

    #Frågar om användaren om hen vill spara sitt lösenord
    remember = BooleanField("Kom ihåg mig")

    submit = SubmitField("Login")

