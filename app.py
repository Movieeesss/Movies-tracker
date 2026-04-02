from flask import Flask
import threading
import os
import movies 

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is Running", 200

@app.route('/run-movies')
def trigger_movies():
    # Background-la run panna thread start panrom
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    # Simple message for Cron-job.org to avoid 'Output too large'
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
