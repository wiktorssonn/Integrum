from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_integrum.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

#Om en sida är login_required kommer man till login sidan
login_manager.login_view = "users.login" 

#Visar ett meddelande när man kommer till sida där man måste logga in
login_manager.login_message_category = "info" 

#Skickar mejl med länk för återställning av lösenord
mail = Mail()


#Funktionen som skapar själva applikationen/hemsidan
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_integrum.users.routes import users
    from flask_integrum.posts.routes import posts
    from flask_integrum.users.routes import users
    from flask_integrum.main.routes import main
    from flask_integrum.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
