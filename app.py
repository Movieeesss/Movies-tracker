from flask import Flask
import threading
import os

# --- IMPORTING MOVIE SCRAPER ONLY ---
try:
    import movies # movies.py file-ah mattum import panrom
except ImportError:
    movies = None

app = Flask(__name__)

@app.route('/')
def home():
    return "🎬 Uniq Designs - Movie Bot Server is Live!"

# --- ENDPOINT FOR MOVIE TIMINGS ---
@app.route('/run-movies')
def trigger_movies():
    if movies:
        # Threading use panrom Render timeout thavirkka
        threading.Thread(target=movies.run_all).start()
        return "🎬 Movie Update Triggered! Check Telegram."
    else:
        return "❌ Error: movies.py file not found in repository!"

if __name__ == "__main__":
    # Render requirements-ku yetha maadhiri port set panrom
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
