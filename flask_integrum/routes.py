import os
#Används för att göra om filnamn till ett random hextal/hexsträng
import secrets
#För att skala profilbilderna
from PIL import Image

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_integrum import app, db, bcrypt, mail
from flask_integrum.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_integrum.models import User, Post
#Används för att logga in användaren
from flask_login import login_user, current_user, logout_user, login_required
#För att skicka mail genom flask_mail
from flask_mail import Message



@app.route("/hem")
def hem():
    return render_template("index.html")

@app.route("/ia")
def ia():
    return render_template("ia.html", title="Informationsarkitekt")

@app.route("/schema")
def schema():
    return render_template("schema.html", title="Schema")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html", title="Calendar")

@app.route("/om_oss")
def om_oss():
    return render_template("om_oss.html", title="Om Oss")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", title="Kontakt")

@app.route("/forum")
def forum():
    #Sätter sida 1 till default, försöker man ange något annat än en int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    #Hämtar inlägg från databasen och sorterar efter senaste datum, paginate ger oss möjlighet att styra hur många inlägg som ska visas per sida etc.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template("forum.html", title="Forum", posts=posts)
    
@app.route("/faq")
def faq():
    return render_template("faq.html", title="FAQ")

@app.route("/todo")
def todo():
    return render_template("todo.html", title="Att göra")

@app.route("/uppgift")
def uppgift():
    return render_template("uppgift.html", title="Uppgift")

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
        flash("Konto skapat med användarnamn '{}'".format(form.username.data), "success")
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
    return redirect(url_for("login"))

#Funktion för att spara ner profilbilderna som laddas upp
def save_picture(form_picture):
    #Sparar den uppladdade bilden som en 8-bitars hex
    random_hex = secrets.token_hex(8)
    #Tar ut file extenstion från bilden som laddas upp
    _, f_ext = os.path.splitext(form_picture.filename)
    #Lägger ihop random_hex med file extension, alltså jpg eller png och sparar i variabeln picture_fn
    picture_fn = random_hex + f_ext
    #Sökvägen till var vi lagrar profilbilderna
    picture_path = os.path.join(app.root_path, "static/images/profile_pics", picture_fn)

    #Skalar ner bilden till angiven storlek
    output_size = (175, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #Sparar ner bilden till sökvägen ovan
    i.save(picture_path)
    
    return picture_fn


@app.route("/profil", methods=["GET", "POST"])
@login_required #Måste vara inloggad för att komma åt sin profil
def profil():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #Om där finns en bild att ladda upp, spara ner filen och uppdatera profilbild
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        #Om formuläret validerat, ersätt med data från formuläret
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash("Ditt konto har uppdaterats!", "success")
        return redirect(url_for("profil"))
        
    #Fyller i fälten med current användarnamn och email
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    #Default profilbild hämtas från databasen om profilbild inte laddas upp av användaren
    image_file = url_for("static", filename="images/profile_pics/" + current_user.image_file)

    return render_template("profil.html", title="Min profil", image_file=image_file, form=form)



@app.route("/create_post", methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Ditt inlägg har publicerats!", "success")
        return redirect(url_for("forum"))
    return render_template("create_post.html", title="Nytt inlägg", form=form, legend="Nytt Inlägg")


#Varje post får en unik sökväg
@app.route("/post/<int:post_id>")
def post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


#Uppdatera inlägg
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    #Om skaparen av inlägget inte är inloggad användare, raise felmeddelande
    if post.author != current_user:
        abort(403)
    form = PostForm()
    #Om uppdateringen validerar, uppdatera inlägg
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Inlägget har uppdaterats!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        #Fyller i fälten med texten som finns i nuläget
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Uppdatera Inlägg")

#Ta bort inlägg
@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    #Om skaparen av inlägget inte är inloggad användare, raise felmeddelande
    if post.author != current_user:
        abort(403)
    #Tar bort inlägget
    db.session.delete(post)
    db.session.commit()
    flash("Ditt inlägg är borttaget!", "success")
    return redirect(url_for("forum"))


#Visar alla inlägg en viss användare gjort (När man klickar på användarnamnet på ett inlägg)
@app.route("/user/<string:username>")
def user_posts(username):
    #Sätter sida 1 till default, försöker man ange något annat än en int blir det ValueError.
    page = request.args.get("page", 1, type=int)
    #Om användaren inte hittas, returnera en 404-error
    user = User.query.filter_by(username=username).first_or_404()
    #Hämtar inlägg från databasen och sorterar efter senaste datum, paginate ger oss möjlighet att styra hur många inlägg som ska visas per sida etc.
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


#Skickar mail till användaren som vill återställa lösenord
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Återställ Lösenord", sender="noreply@integrum.com", recipients=[user.email])
    #_external=True används för att göra url:en absolut
    msg.body = f''' För att återställa ditt lösenord, klicka på länken: {url_for("reset_token", token=token, _external=True)}

    Om du inte skickat en förfrågan om att återställa ditt lösenord, ignorera detta meddelande så kommer inga ändringar att göras.
    '''
    #Skickar mailet
    mail.send(msg)

#Formuläret om förfrågan att återställa lösenordet, validering av email för att kontrollera att kontot finns
@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    form = RequestResetForm()
    if form.validate_on_submit():
        #Om formuläret validerat, hämta ut angiven email från databasen och lagrar i variabeln "user"
        user = User.query.filter_by(email=form.email.data).first()
        #Skicka email till användaren
        send_reset_email(user)
        flash("Ett email har skickats med instruktioner för att återställa lösenordet!", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Återställ Lösenord", form=form)


#Formuläret där återställningen av lösenordet faktiskt sker, anger nytt lösenord
@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    user = User.verify_reset_token(token)
    if user is None:
        #Om user = None, alltså om token är fel eller har utgått visa felmeddlenade och returnera sidan för att återställa lösenord
        flash("Återställningsnyckeln är felaktig eller har utgått!", "warning")
        return redirect(url_for("reset_request"))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Krypterar lösenordet som skrivs in i formuläret, görs om till sträng
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Ditt lösenord har uppdaterats!", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Återtställ Lösenord", form=form)





#pip install Flask

#pip install Flask-WTF      -Validering av formulär etc

#pip install flask-bcrypt       -Kryptering av lösenord 

#pip install flask-sqlalchemy   -Databas

#pip install flask-login    -Loginfunktioner

#pip install Pillow     -Gör att vi kan skala profilbilderna

#pip install flask-mail     -För att skicka mail genom flask
