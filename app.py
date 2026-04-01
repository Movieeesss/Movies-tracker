from flask import Flask
import os
import importlib
import movies # Direct import
import bot    # Direct import

app = Flask(__name__)

@app.route('/')
def home():
    return "Trichy Tracker is Active!"

@app.route('/run-steel')
def run_steel():
    try:
        importlib.reload(bot)
        # Indha line-ah unga bot.py-la irukka function name-ku mathunom
        bot.send_update() 
        return "Steel Bot Executed Successfully!"
    except Exception as e:
        return f"Steel Bot Error: {str(e)}"

@app.route('/run-movies')
def run_movies():
    try:
        importlib.reload(movies)
        # UNGA MOVIES.PY-LA IRUKKA REAL FUNCTION NAME:
        movies.send_update() 
        return "Movie Bot Executed Successfully!"
    except Exception as e:
        return f"Movie Bot Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
