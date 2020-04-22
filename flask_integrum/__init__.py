import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config["SECRET_KEY"] = "fbc07874e91feeaa1b0e8dcb400930bf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" #Om en sida är login_required kommer man till login sidan
login_manager.login_message_category = "info" #Visar ett meddelande när man kommer till en sida där man måste logga in

#Inställningar för att skicka mail via gmail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "integrumnoreply@gmail.com"
app.config["MAIL_PASSWORD"] = "integrum1337"
mail = Mail(app)


from flask_integrum import routes