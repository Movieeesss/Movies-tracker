from flask import Flask, jsonify, request
import threading
import os
import movies
import json

app = Flask(__name__)
USER_FILE = "users.json"

def save_user(chat_id):
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                users = json.load(f)
            except: users = []
    
    if chat_id not in users:
        users.append(chat_id)
        with open(USER_FILE, "w") as f:
            json.dump(users, f)

@app.route('/')
def home():
    return "Movie Tracker is Live!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            save_user(chat_id)
            import requests
            requests.post(f"https://api.telegram.org/bot{movies.TOKEN}/sendMessage", 
                          data={"chat_id": chat_id, "text": "Welcome! Inime Trichy movies update ungaluku auto-va varum. 🎬"})
            
    return "OK", 200

@app.route('/run-movies')
def trigger_movies():
    # Threading problem-ah thavirkka direct-ah run panrom
    movies.run_all()
    return jsonify({"status": "Success", "message": "Updates sent to all users"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
