import os
from flask import Flask
import threading
from movies import run_all

app = Flask(__name__)

@app.route('/')
def home():
    return "Movie Tracker is Live!"

@app.route('/run-movies')
def trigger_movies():
    # Background-la oduna thaan Cron-job timeout aagathu
    thread = threading.Thread(target=run_all)
    thread.start()
    return "Scraper Started Successfully", 200

if __name__ == "__main__":
    # RENDER FIX: Dynamic port binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
