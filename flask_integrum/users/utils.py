import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_integrum import mail



#Funktion för att spara ner profilbilderna som laddas upp
def save_picture(form_picture):
    #Sparar den uppladdade bilden som en 8-bitars hex
    random_hex = secrets.token_hex(8)
    #Tar ut file extenstion från bilden som laddas upp
    _, f_ext = os.path.splitext(form_picture.filename)
    #Lägger ihop random_hex med file extension, alltså jpg eller png och sparar i variabeln picture_fn
    picture_fn = random_hex + f_ext
    #Sökvägen till var vi lagrar profilbilderna
    picture_path = os.path.join(current_app.root_path, "static/images/profile_pics", picture_fn)

    #Skalar ner bilden till angiven storlek
    output_size = (175, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #Sparar ner bilden till sökvägen ovan
    i.save(picture_path)
    
    return picture_fn


#Skickar mail till användaren som vill återställa lösenord
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Återställ Lösenord", sender="noreply@integrum.com", recipients=[user.email])
    #_external=True används för att göra url:en absolut
    msg.body = f''' För att återställa ditt lösenord, klicka på länken: {url_for("users.reset_token", token=token, _external=True)}
    Om du inte skickat en förfrågan om att återställa ditt lösenord, ignorera detta meddelande så kommer inga ändringar att göras.
    '''
    #Skickar mailet
    mail.send(msg)


