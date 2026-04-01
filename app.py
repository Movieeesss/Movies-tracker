from flask import Flask
import threading
import os

try:
    import movies
except ImportError:
    movies = None

app = Flask(__name__)

@app.route('/')
def home():
    return "OK"

@app.route('/run-movies')
def trigger_movies():
    if movies:
        # Background-la scraper run aagum
        threading.Thread(target=movies.run_all).start()
        # Cron-job ku chinna response mattum anuppurom
        return "OK", 200
    return "Error", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
