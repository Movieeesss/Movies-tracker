from flask import Flask
import movies
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ App Running"

@app.route('/run')
def run():
    try:
        print("🔥 RUN TRIGGERED")
        movies.run_all()
        return "✅ SUCCESS"
    except Exception as e:
        print("❌ ERROR:", str(e))
        print(traceback.format_exc())
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    app.run()
