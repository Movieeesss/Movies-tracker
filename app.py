from flask import Flask
import bot  # Steel scraper
import movies # Movie scraper
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Uniq Designs Bot Server is Live!"

@app.route('/run-steel')
def trigger_steel():
    # Running in thread to avoid Render timeout
    threading.Thread(target=bot.send_update).start()
    return "Steel Update Triggered!"

@app.route('/run-movies')
def trigger_movies():
    threading.Thread(target=movies.run_all).start()
    return "Movie Update Triggered!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
