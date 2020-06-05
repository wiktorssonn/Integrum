# Integrum

Systemutveckling och Projekt - Integrum

Skapa en enklare och mer användbar "Canvas" främst för Informationsarkitekter.

Instruktioner för att öppna programmet via Flask (om du jobbar via GitHub):
---------------------------------------------------------------------------
1. Börja med att installera alla pip installs som krävs för att starta servern.
   Efter att du laddat ner filen från github, börja med att navigera till 
   integrum mappen i valfri terminal/kommandotolk och skriv sedan i
   terminalen: pip install -r requirements.txt

2. När alla pip installs är klara, skriv: python3 app.py eller python app.py för att starta servern.
 
3. Om servern startar utan några felmeddelande, öppna valfri webbläsare och surfa till
   127:0:0:1:5000
   
4. Om du får upp felmeddelande om att någon modul saknas, läs vilken modul som saknas och skriv
   pip install <saknad_modul> och upprepa steg 2 igen.


Programmet är byggt med Python biblioteket Flask och måste därför startas via en terminal tills vidare utveckling möjliggör andra startalternativ.
Alla HTML sidor ligger i mappen templates. För att ändra den övergripande strukturen på samtliga sidor skall endast "layout" ändras. 
Om mindre eller unika ändringar skall ske för en specifik sida så ändras detta i respektive HTML dokument (t.ex schema.html).
Använd då följande exempel för att lägga in nya element, där "text" är exempel på det som blir unikt på respektive sida. Övrigt utseende
tas från layout.html som ligger som grund för samtliga sidor.
    
    {% extends "layout.html" %}
        
    {% block content %}

        <p>text</p>

    {% endblock content %}
    
   
Länk till github repository: https://github.com/wiktorssonn/Integrum
Kod för databasen ligger i filen "models.py" 
