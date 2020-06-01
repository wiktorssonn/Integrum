from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_integrum import db, bcrypt
from flask_integrum.models import User, Post
from flask_integrum.users.forms \
    import (RegistrationForm, LoginForm, UpdateAccountForm,
            RequestResetForm, ResetPasswordForm)
from flask_integrum.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)



@users.route("/register", methods=["GET", "POST"])
def register():
    #Om användaren redan är inloggad
    #kommer man inte till inloggningen igen
    if current_user.is_authenticated:
        return redirect(url_for("main.hem"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Krypterar lösenordet i formuläret, görs om till sträng
        hashed_password = \
                        bcrypt.generate_password_hash \
                        (form.password.data).decode("utf-8")
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Konto skapat med användarnamn '{}'" \
            .format(form.username.data), "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", 
                            title="Registrera", 
                            form=form)



#Sidan för att logga in, är även startsidan
@users.route("/")
@users.route("/login", methods=["GET", "POST"])
def login():
    #Om användaren redan är inloggad 
    #kommer man inte till inloggningen igen
    if current_user.is_authenticated:
        return redirect(url_for("main.hem"))
    form = LoginForm()
    if form.validate_on_submit():
        #Kontrollerar att där finns en email i 
        #databasen som stämmer överens med angiven email
        user = User.query.filter_by(email=form.email.data).first()
        #Om emailen finns, kontrollera att 
        #lösenordet i databasen matchar angivet lösenord
        if user and bcrypt.check_password_hash \
        (user.password, form.password.data):
            flash("Du är nu inloggad!", "success")
            #Loggar in användaren,
            #remember är valet om man vill komma ihåg användaren
            login_user(user, remember=form.remember.data)
            #Om man kommer till en sida som kräver inloggning
            #tas man vidare till den sidan 
            #efter inloggning istället för "hem"
            next_page = request.args.get("next")
            return redirect(next_page) \
            if next_page else redirect(url_for("main.hem"))      
        else:
            flash("Inloggningen misslyckades," \
                    "kontrollera email och lösenord!", "danger")
    return render_template("login.html", title="Logga in", form=form)



#Om användaren trycker på logga ut
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))



#Profilsidan för varje användare
@users.route("/profil", methods=["GET", "POST"])
@login_required #Måste vara inloggad för att komma åt sin profil
def profil():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #Om där finns en bild att ladda upp, 
            #Spara ner filen och uppdatera profilbild
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        #Om formuläret validerat, ersätt med data från formuläret
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash("Ditt konto har uppdaterats!", "success")
        return redirect(url_for("users.profil"))
        
    #Fyller i fälten med current användarnamn och email
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    #Default profilbild hämtas från databasen 
    #Om profilbild inte laddas upp av användaren
    image_file = url_for("static", 
                        filename="images/profile_pics/" \
                        + current_user.image_file)

    return render_template("profil.html", 
                            title="Min profil", 
                            image_file=image_file, 
                            form=form)



#Visar alla inlägg en viss användare gjort 
#(När man klickar på användarnamnet på ett inlägg)
@users.route("/user/<string:username>")
def user_posts(username):
    #Sätter sida 1 till default, 
    #Försöker man ange något annat än en int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    #Om användaren inte hittas, returnera en 404-error
    user = User.query.filter_by(username=username).first_or_404()
    #Hämtar inlägg från databasen och sorterar efter senaste datum, 
    #Paginate ger oss möjlighet att styra hur
    #Många inlägg som ska visas per sida etc.
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", 
                            posts=posts, 
                            user=user)



#Formuläret om förfrågan att återställa lösenordet,
#Validering av email för att kontrollera att kontot finns
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.hem"))
    form = RequestResetForm()
    if form.validate_on_submit():
        #Om formuläret validerat, 
        #Hämta ut angiven email från databasen och
        #Lagrar i variabeln "user"
        user = User.query.filter_by(email=form.email.data).first()
        #Skicka email till användaren
        send_reset_email(user)
        flash("Ett email har skickats med " \
                "instruktioner för att återställa lösenordet!", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", 
                            title="Återställ Lösenord", 
                            form=form)



#Formuläret där återställningen av lösenordet faktiskt sker, 
#Anger nytt lösenord
@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.hem"))
    user = User.verify_reset_token(token)
    if user is None:
        #Om user = None, alltså om token är fel eller har utgått 
        #Visa felmeddlenade och returnera sidan
        #För att återställa lösenord
        flash("Återställningsnyckeln är" \
                "felaktig eller har utgått!", "warning")
        return redirect(url_for("users.reset_request"))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Krypterar lösenordet som skrivs in i formuläret,
        #Görs om till sträng
        hashed_password = bcrypt.generate_password_hash \
                            (form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Ditt lösenord har uppdaterats!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", 
                            title="Återtställ Lösenord", 
                            form=form)