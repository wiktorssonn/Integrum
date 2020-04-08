from flask_integrum import db, login_manager
#Funktioner för att kontrollera att användaren är autentiserad etc.
from flask_login import UserMixin

#Hämtar ut användare genom id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    #Hur vår model printas ut
    def __repr__(self):
        return "User('{}', '{}', '{}')" .format(self.username, self.email, self.image_file)

