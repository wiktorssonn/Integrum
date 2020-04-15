from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_integrum import app, db, bcrypt
from flask_integrum.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm
from flask_integrum.models import User, Post
#Används för att logga in användaren
from flask_login import login_user, current_user, logout_user, login_required
#Används för att göra om filnamn till ett random hextal/hexsträng
import secrets
import os
#För att skala profilbilderna
from PIL import Image



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
    #Hämtar alla inlägg från databasen
    posts = Post.query.all()
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



@app.route("/create_post", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ditt inlägg har publicerats!', 'success')
        return redirect(url_for('forum'))
    return render_template('create_post.html', title='Nytt inlägg', form=form, legend="Nytt Inlägg")


#Varje post får en unik sökväg
@app.route("/<int:post_id>")
def post(post_id):
    #Om sökvägen inte finns, returnera 404
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


#Uppdatera inlägg
@app.route("/<int:post_id>/update", methods=["GET", "POST"])
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
@app.route("/<int:post_id>/delete", methods=["GET", "POST"])
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







#pip install Flask

#pip install Flask-WTF      -Validering av formulär etc

#pip install flask-bcrypt       -Kryptering av lösenord 

#pip install flask-sqlalchemy   -Databas

#pip install flask-login    -Loginfunktioner

#pip install Pillow     -Gör att vi kan skala profilbilderna

