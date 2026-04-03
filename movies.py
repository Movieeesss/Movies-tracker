import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"
USER_FILE = "users.json"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_list = set() 
    try:
        response = requests.get(proxy_url, timeout=45)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                if 2 < len(name) < 50:
                    blacklist = ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST", "BMS", "SCREEN"]
                    if not any(x in name for x in blacklist):
                        movie_list.add(name)
        else:
            print(f"Scraper Error: Status {response.status_code}")
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No movies detected.\n"
    else:
        body = "🎥 *NOW SHOWING:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    final_msg = header + meta + body + footer

    # MULTIPLE USERS-ku anuppura logic
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                users = json.load(f)
            except: users = []
            
        for user_id in users:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                    data={"chat_id": user_id, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"}
                )
            except Exception as e:
                print(f"Error sending to {user_id}: {e}")

if __name__ == "__main__":
    run_all()
