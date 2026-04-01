from flask import Flask
import movies

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Trichy Movie Bot Running!"

@app.route('/run')
def run():
    try:
        movies.run_all()
        return "✅ Movie bot executed"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    app.run()
