from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "fbc07874e91feeaa1b0e8dcb400930bf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db= SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self): #Hur det printas ut?
        return User("{}, {}, {}, {}".format(self.username, self.email, self.image_file))




@app.route("/")
@app.route("/hem")
def hem():
    return render_template("index.html")


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
        flash("Account created for {}!".format(form.username.data, "success"))
        return redirect(url_for("hem"))
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
#pip install Flask-WTF
#pip install WTForms
#pip install flask-sqlalchemy