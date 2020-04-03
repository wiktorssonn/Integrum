from flask import Flask, render_template, url_for, flash, redirect

from forms import RegistrationForm, LoginForm, ValidationError
#Kryperar användarnas lösenord
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
app.config["SECRET_KEY"] = "fbc07874e91feeaa1b0e8dcb400930bf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
#db= SQLAlchemy(app)
bcrypt = Bcrypt(app)

'''
#Connecting to database
try:
    connection = psycopg2.connect(user = "aj8772",
                              password = "z7zz9fgh",
                              host = "pgserver.mah.se",
                              database = "integrum_db")
    cursor = connection.cursor()
    print("Connected to database")
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
'''

#cursor.execute("create table users (user_id serial primary key, username varchar(20) unique not null, email varchar(120) not null, password varchar(60) not null)")
#connection.commit()
#route_records = cursor.fetchall()

'''class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self): #Hur det printas ut?
        return User("{}, {}, {}, {}".format(self.username, self.email, self.image_file))
'''




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
        if form.email.data == "blabla@gmail.com" and form.password.data == "password":
            flash("Inloggning lyckades!", "success")
            return redirect(url_for("hem"))
        else:
            flash("Inloggning misslyckades, Kontrollera användarnamn och lösenord", "danger")
    return render_template("login.html", title="Logga in", form=form)


@app.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")


if __name__ == "__main__":  # Startar servern automatiskt och kör den i debug-mode
    app.run(debug=True)


#pip install Flask

#pip install Flask-WTF      -Validering av formulär etc

#pip install flask-bcrypt       -Kryptering av lösenord 


