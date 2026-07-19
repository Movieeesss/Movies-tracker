import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
USER_FILE = "users.json"
MY_ID = 8095698350  # Unga permanent ID

def get_trichy_movies():
    # URL updated to Trichy
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    
    # Changed proxy=residential to proxy=stealth to bypass Cloudflare
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=stealth&render=true&wait=10000"
    
    movie_list = set() 
    try:
        # Increased timeout to 60s because stealth proxies can take slightly longer
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            # Debugging checks
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by BookMyShow Anti-bot (Cloudflare).")
                return []
            
            if "error" in response.text.lower() and "api" in response.text.lower():
                print(f"⚠️ API ERROR: {response.text}")
                return []

            # Proceed to parse if no blocks
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                if 2 < len(name) < 50:
                    blacklist = ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST", "BMS", "SCREEN"]
                    if not any(x in name for x in blacklist):
                        movie_list.add(name)
                        
            if not movie_list:
                print("⚠️ WARNING: Page loaded, but no <h3> movie tags were found. Structure might have changed.")
                
        else:
            print(f"⚠️ Scraper Error: HTTP Status Code {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Network/Scraper Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No movies detected. (Possible API Block or Empty List)\n"
    else:
        body = "🎥 *NOW SHOWING:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    final_msg = header + meta + body + footer

    user_list = [MY_ID]
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                extra_users = json.load(f)
                for u in extra_users:
                    if u not in user_list:
                        user_list.append(u)
            except: pass
            
    for user_id in user_list:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={"chat_id": user_id, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"}
            )
        except: pass

if __name__ == "__main__":
    run_all()
