from flask import Flask, jsonify, request
import threading
import os
import movies
import json
import requests # Global-ah import pannikonga

app = Flask(__name__)
USER_FILE = "users.json"

# User ID save panna logic
def save_user(chat_id):
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    
    if chat_id not in users:
        users.append(chat_id)
        with open(USER_FILE, "w") as f:
            json.dump(users, f)

@app.route('/')
def home():
    return "Movie Tracker is Live!", 200

# Webhook for /start command
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            save_user(chat_id)
            # Welcome message sending
            try:
                requests.post(f"https://api.telegram.org/bot{movies.TOKEN}/sendMessage", 
                              data={"chat_id": chat_id, "text": "Welcome! Inime Trichy movies update ungaluku auto-va varum. 🎬"})
            except:
                pass
            
    return "OK", 200

# Main trigger with threading and minimal response size
@app.route('/run-movies')
def trigger_movies():
    try:
        # Background-la movies run aagum (Render 'Freeze' aagama irukka threading best)
        thread = threading.Thread(target=movies.run_all)
        thread.start()
        
        # Cron-job.org-kaga romba chinna response "OK" mattum anupuvom
        return "OK", 200 
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
