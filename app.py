from flask import Flask
import os
import importlib

app = Flask(__name__)

@app.route('/')
def home():
    return "Trichy Tracker is Active!"

@app.route('/run-steel')
def run_steel():
    try:
        # bot.py-ah direct-ah import panni run panrom
        import bot
        importlib.reload(bot)
        bot.send_update()
        return "Steel Bot Executed Successfully!"
    except Exception as e:
        return f"Steel Bot Error: {str(e)}"

@app.route('/run-movies')
def run_movies():
    try:
        # movies.py-ah direct-ah import panni run panrom
        import movies
        importlib.reload(movies)
        movies.send_telegram() # Unga movies.py-la intha function name check pannikonga
        return "Movie Bot Executed Successfully!"
    except Exception as e:
        return f"Movie Bot Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
