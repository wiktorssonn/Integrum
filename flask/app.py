from flask import Flask, render_template, url_for, flash, redirect

from forms import RegistrationForm, LoginForm, ValidationError
#Kryperar användarnas lösenord
from flask_bcrypt import Bcrypt
#Login funktion
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
#Importerar psycopg2 för att skriva till databasen
import psycopg2


app = Flask(__name__)
app.config["SECRET_KEY"] = "fbc07874e91feeaa1b0e8dcb400930bf"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@app.route("/")
@app.route("/hem")
def hem():
    return render_template("index.html")

@app.route("/schema")
def schema():
    return render_template("schema.html", title="Schema")


@app.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Krypterar lösenordet som skrivs in i formuläret, görs om till sträng
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
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

        #Tar emot det som fyllts i och validerats under registrering och lägger till i users table
        cursor.execute("insert into users (username, email, password)values ('{}', '{}', '{}')".format(form.username.data, form.email.data, hashed_password))
        connection.commit()
        
        #Ska visa tillfälligt meddelande att skapandet lyckades (Fungerar inte)
        flash("Your account has been created! You are now able to log in {}!".format(form.username.data, "success")) 
        return redirect(url_for("login"))
    return render_template("register.html", title="Registrera", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        '''
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
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        print("Email: {}".format(email))
        print("Lösenord: {}".format(password))


        #Hämtar alla email från users table i databasen
        cursor.execute("select * from users")
        all_users = cursor.fetchall()
        
        user_exist = False
        for user in all_users:
            if email.lower() == user[2].lower and password == user[3]:
                print(user[2],user[3])
                user_exist = True
            else:
                print(user[2],user[3])
                print("hej")
        #Om emailen redan finns, skriv ut felmeddelande
        #if email_in_use == True:
            #raise ValidationError("Denna mail finns redan registrerad!")
        
        
        
        user = User.query.filter_by(username=username.lower()).first()
        if user:
            if login_user(user):
                flash("Inloggning lyckades!", "success")
                return redirect(url_for("hem"))
        else:
            flash("Inloggning misslyckades, Kontrollera användarnamn och lösenord", "danger")'''
    return render_template("login.html", title="Logga in", form=form)


@app.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")


if __name__ == "__main__":  # Startar servern automatiskt och kör den i debug-mode
    app.run(debug=True)


#pip install Flask

#pip install Flask-WTF      -Validering av formulär etc

#pip install flask-bcrypt       -Kryptering av lösenord 


