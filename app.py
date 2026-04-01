from flask import Flask
import os
import importlib
import movies 

app = Flask(__name__)

@app.route('/')
def home():
    return "Trichy Tracker Active!"

@app.route('/run-movies')
def run_movies():
    try:
        importlib.reload(movies)
        movies.run_all() # Matches the function name in movies.py
        return "Movie Bot Success!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
