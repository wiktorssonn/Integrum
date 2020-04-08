from flask import Flask, render_template, url_for, flash, redirect, request
from flask_integrum import app, db, bcrypt
from flask_integrum.forms import RegistrationForm, LoginForm
from flask_integrum.models import User
#Används för att logga in användaren
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/hem")
def hem():
    return render_template("index.html")


@app.route("/ia")
def ia():
    return render_template("ia.html", title="Informationsarkitekt")

@app.route("/schema")
def schema():
    return render_template("schema.html", title="Schema")


@app.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")

@app.route("/forum")
def forum():
    return render_template("forum.html", title="Forum")


@app.route("/register", methods=["GET", "POST"])
def register():
    #Om användaren redan är inloggad kommer man inte till inloggningen igen
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Krypterar lösenordet som skrivs in i formuläret, görs om till sträng
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Konto skapat med användarnamn {}".format(form.username), "sucess")
        return redirect(url_for("login"))
    return render_template("register.html", title="Registrera", form=form)

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    #Om användaren redan är inloggad kommer man inte till inloggningen igen
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    form = LoginForm()
    if form.validate_on_submit():
        #Kontrollerar att där finns en email i databasen som stämmer överens med angiven email
        user = User.query.filter_by(email=form.email.data).first()
        #Om emailen finns, kontrollera att lösenordet i databasen matchar angivet lösenord
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("Du är nu inloggad!", "success")
            #Loggar in användaren, remember är valet om man vill komma ihåg användaren
            login_user(user, remember=form.remember.data)
            #Om man kommer till en sida som kräver inloggning tas man vidare till den sidan efter inloggning istället för "hem"
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("hem"))      
        else:
            flash("Inloggningen misslyckades, kontrollera email och lösenord!", "danger")
    return render_template("login.html", title="Logga in", form=form)


#Om användaren trycker på logga ut
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("hem"))


@app.route("/profil")
@login_required #Måste vara inloggad för att komma åt sin profil
def konto():
    return render_template("profil.html", title="Min profil")


@app.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")



#pip install Flask

#pip install Flask-WTF      -Validering av formulär etc

#pip install flask-bcrypt       -Kryptering av lösenord 

#pip install flask-sqlalchemy   -Databas

#11:15 - 


