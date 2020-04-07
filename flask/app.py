from flask import Flask, render_template, url_for, flash, redirect

from forms import RegistrationForm, LoginForm, ValidationError, PostForm
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

@app.route("/ia")
def ia():
    return render_template("ia.html", title="Informationsarkitekt")

@app.route("/schema")
def schema():
    return render_template("schema.html", title="Schema")

@app.route("/todo")
def todo():
    return render_template("todo.html", title="Todo")

@app.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")

@app.route("/forum")
def forum():
    return render_template("forum.html", title="Forum")

@app.route("/new_post", methods=['GET','POST'])
def new_post():
    form = PostForm()
    return render_template("create_post.html", title="New Post", form =form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/profil")
def profile():
    return render_template("profile.html", title="Profil")


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
        password = form.password.data

        #Hämtar alla email från users table i databasen
        cursor.execute("select * from users")
        all_users = cursor.fetchall()
    
        for user in all_users:
            #Kontrollerar att email och lösenord stämmer överens med email och lösenord i databasen
            #Jämför lösenordet som skrivits in gentemot det krypterade lösenordet i databasen
            if email.lower() == user[2].lower() and bcrypt.check_password_hash(user[3], password):
                flash("Inloggning lyckades!", "success")
                return redirect(url_for("hem"))
            #Om inte email och lösenord matchar så ska flash-meddelande komma upp
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



