import os
from flask import Flask
import threading
from movies import run_all

app = Flask(__name__)

@app.route('/')
def home():
    return "Movie Tracker is Active!"

@app.route('/run-movies')
def trigger_movies():
    # Threading use pannuraathaala Cron-job timeout aagaathu
    thread = threading.Thread(target=run_all)
    thread.start()
    return "Scraper Started", 200

if __name__ == "__main__":
    # Render-ku PORT env variable romba mukkiyam
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
