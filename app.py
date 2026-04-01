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
        # 1. Threading starts the scraper in the background
        threading.Thread(target=movies.run_all).start()
        
        # 2. Immediate tiny response to Cron-job (Fixes "Output too large")
        return "OK", 200
    else:
        # Error response if file is missing
        return "ERROR: movies.py missing", 404

if __name__ == "__main__":
    # Render dynamic port binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
