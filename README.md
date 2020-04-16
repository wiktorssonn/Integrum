# Integrum

Systemutveckling och Projekt - Integrum

Skapa en enklare och mer användbar "Canvas" främst för Informationsarkitekter.

Instruktioner för att öppna programmet via Flask (om du jobbar via GitHub):
---------------------------------------------------------------------------
1. Skriv "python app.py" alternativt "python3 app.py" i terminalen (Funkar inte detta så är du inte i rätt directory).
2. Om inte 1 fungerar skriv "ls" i terminalen för att se var du står just nu. Navigera sedan till /Users/användarnamn/Documents/GitHub/Integrum/flask_integrum med hjälp av "cd" kommandot. (För att gå tillbaka skriv "cd .." på Windows och cd ../ på Mac, cd ../../ tar dig två steg tillbaka) Se guide om navigering via terminal, https://courses.cs.washington.edu/courses/cse140/13wi/shell-usage.html
3. Skriv python3 app.py för att starta applikationen och surfa in på http://127.0.0.1:5000.
4. Om ovanstånde inte funkar så är du antagligen fortfarande i fel directory. Följ då steg 2 till 3 igen.
5. Om det fortfarande inte fungerar så behövs antagligen moduler installeras (se Pip-installs som behövs längre ner på denna sidan).


Pip-installs som behövs:

pip install Flask

pip install Flask-WTF      -Validering av formulär etc

pip install flask-bcrypt       -Kryptering av lösenord 

pip install flask-sqlalchemy   -Databas

pip install flask-login    -Loginfunktioner

pip install Pillow     -Gör att vi kan skala profilbilderna


XML Kronox = https://schema.mau.se/appserver-ejb/RapportEJB?wsdl


Programmet är byggt med Python biblioteket Flask och måste därför startas via en terminal tills vidare utveckling möjliggör andra startalternativ.
Alla HTML sidor ligger i mappen templates. För att ändra den övergripande strukturen på samtliga sidor skall endast "layout" ändras. 
Om mindre eller unika ändringar skall ske för en specifik sida så ändras detta i respektive HTML dokument (t.ex schema.html).
Använd då följande exempel för att lägga in nya element, där "text" är exempel på det som blir unikt på respektive sida. Övrigt utseende
tas från layout.html som ligger som grund för samtliga sidor.
    
    {% extends "layout.html" %}
        
    {% block content %}

        <p>text</p>

    {% endblock content %}
