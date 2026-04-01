from flask import Flask
import threading
import os
import movies # Unga movies.py file-ah import pannuthu

app = Flask(__name__)

@app.route('/')
def home():
    return "Movie Tracker is Live!", 200

@app.route('/run-movies')
def trigger_movies():
    # Background Thread: Ithu thaan cron-job timeout aagaama thadukkum
    # Hit panna udane 'OK' response anuppidum, scraper background-la run aagum
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    return "Scraper Started in Background", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
