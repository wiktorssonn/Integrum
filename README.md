# Integrum

Systemutveckling och Projekt - Integrum

Skapa en enklare och mer användbar "Canvas" främst för Informationsarkitekter.

Instruktioner för att öppna programmet via Flask (om du jobbar via GitHub):
---------------------------------------------------------------------------
1. Skriv python3 app.py i terminalen(Funkar inte detta så är du inte i rätt directory)
2. Om inte 1 fugerar skriv: cd documents/github/integrum/flask
3. Skriv python3 app.py 
4. Om ovanstånde inte funkar så är du fortfarande i fel directory. Skriv då ls för att navigera dig till rätt directory.
5. För att välja ett directory skriver du: cd --namn på directory--



Programmet är byggt med Python biblioteket Flask och måste därför startas via en terminal tills vidare utveckling möjliggör andra startalternativ.
Alla HTML sidor ligger i mappen templates. För att ändra den övergripande strukturen på samtliga sidor skall endast "layout" ändras. 
Om mindre eller unika ändringar skall ske för en specifik sida så ändras detta i respektive HTML dokument (t.ex schema.html).
Använd då följande exempel för att lägga in nya element:
    
    {% extends "layout.html" %}
        
    {% block content %}

        <p>text</p>

    {% endblock content %}