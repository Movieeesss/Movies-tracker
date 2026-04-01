from flask import Flask
import threading
import os
import movies  # Direct-ah import pannunga

app = Flask(__name__)

@app.route('/')
def home():
    return "Service is Running", 200

@app.route('/run-movies')
def trigger_movies():
    # Threading use panna thaan cron-job timeout aagaama background-la run aagum
    threading.Thread(target=movies.run_all).start()
    return "OK - Scraper Started", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
