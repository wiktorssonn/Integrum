
#Konfiguration för applikationen/hemsidan
class Config:
    SECRET_KEY = "fbc07874e91feeaa1b0e8dcb400930bf"
    
    #Postgresql-databasen
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://aj8772:z7zz9fgh@pgserver.mah.se/integrum_db"

    #Inställningar för att skicka mail via gmail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "integrumnoreply@gmail.com"
    MAIL_PASSWORD = "integrum1337"