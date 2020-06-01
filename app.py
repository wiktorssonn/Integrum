from flask_integrum import create_app

app = create_app()

# Startar servern automatiskt och kör den i debug-mode
if __name__ == "__main__":
    app.run(debug=True)