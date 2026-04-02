from flask import Flask
import threading
import os
import movies 

app = Flask(__name__)

@app.route('/')
def home():
    return "LA Cinema LATG Tracker Active", 200

@app.route('/run-movies')
def trigger_movies():
    # Background thread starts scraping
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    # Simple 'OK' avoids 'Output too large' on cron-job.org
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
