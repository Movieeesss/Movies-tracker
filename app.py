from flask import Flask
import threading
import movies # Movie scraper file

# 'bot.py' file illai na error varaama irukka intha logic
try:
    import bot # Steel scraper
except ImportError:
    bot = None

app = Flask(__name__)

@app.route('/')
def home():
    return "Uniq Designs Bot Server is Live!"

@app.route('/run-steel')
def trigger_steel():
    if bot:
        threading.Thread(target=bot.send_update).start()
        return "Steel Update Triggered!"
    else:
        return "Error: bot.py file not found in server!"

@app.route('/run-movies')
def trigger_movies():
    threading.Thread(target=movies.run_all).start()
    return "Movie Update Triggered!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
