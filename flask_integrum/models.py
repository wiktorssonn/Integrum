from flask_integrum import db, login_manager
#Ger oss en nyckel som blir ogiltig efter utsatt tid, 
#för återställning av lösenord
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#Funktioner för att kontrollera att användaren är autentiserad etc.
from flask_login import UserMixin
#Tid och datum
from datetime import datetime
from flask import current_app



#Hämtar ut användare genom id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#Hur vårt "User" table är uppbyggt samt hur det sparas i databasen
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, 
                    primary_key=True)
    username = db.Column(db.String(20), 
                            unique=True, 
                            nullable=False)
    email = db.Column(db.String(120), 
                        unique=True, 
                        nullable=False)
    image_file = db.Column(db.String(20), 
                            nullable=False, 
                            default="default.jpg")
    password = db.Column(db.String(60), 
                            nullable=False)
    posts = db.relationship("Post", 
                            backref="author", 
                            lazy=True)
    todo = db.relationship("Todo", 
                            backref="assignment_author", 
                            lazy=True)

    #Sätter koden som används för återställning 
    #Av lösenord till att gå ut efter 30minuter
    def get_reset_token(self, expires_sec=1800):
        #Hämtar secret_key från init.py genom current_app.config
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    #Verifiera återställningskoden
    #Vi tar bara emot token som argument, inte self
    @staticmethod 
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            #Ta fram token/återställningskod
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    #Hur vår modell skrivs ut
    def __repr__(self):
        return "User('{}', '{}', '{}', {})".format(self.username, 
                                                    self.email, 
                                                    self.image_file, 
                                                    self.id)



#Hur vårt "Post" table är uppbyggt samt hur det sparas i databasen
class Post(db.Model):
    id = db.Column(db.Integer, 
                    primary_key=True)
    title = db.Column(db.String(100), 
                        nullable=False)
    date_posted = db.Column(db.DateTime, 
                            nullable=False, 
                            default=datetime.utcnow)
    content = db.Column(db.Text, 
                        nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("user.id"), 
                        nullable=False)

    #Hur vår modell skrivs ut
    def __repr__(self):
        return "Post('{}, '{}')".format(self.title, self.date_posted)



#Hur vårt "Todo" table är uppbyggt samt hur det sparas i databasen
class Todo(db.Model):
    id = db.Column(db.Integer, 
                    primary_key=True)
    assignment = db.Column(db.String(100), 
                            nullable=False)
    description = db.Column(db.Text, 
                            nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("user.id"), 
                        nullable=False)
    completed = db.Column(db.Boolean)
    
    #Hur vår modell skrivs ut
    def __repr__(self):
        return "Todo('{}, '{}', {})".format(self.assignment, 
                                            self.description, 
                                            self.user_id)