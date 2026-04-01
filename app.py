from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Trichy Tracker is Running on Render!"

# Steel bot trigger
@app.route('/run-steel')
def run_steel():
    subprocess.Popen(['python', 'bot.py'])
    return "Steel Bot Started!"

# Movie bot trigger
@app.route('/run-movies')
def run_movies():
    subprocess.Popen(['python', 'movies.py'])
    return "Movie Bot Started!"

if __name__ == "__main__":
    # Render automatic-ah port assign pannum, adhai Flask eduthukkum
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
