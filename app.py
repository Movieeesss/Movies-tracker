from flask import Flask
import threading
import os
import movies 

app = Flask(__name__)

@app.route('/')
def home():
    return "LA Cinema Live Tracker Running", 200

@app.route('/run-movies')
def trigger_movies():
    # Run scraper in background to avoid timeout
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    # Return minimal response for Cron-job.org
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
