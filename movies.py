import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
API_KEY = "MKDCNDT9VWVFGX57CQ5NCR9R40F4FZWHDSLF98Z1KEK0NN5F9ZNKOM6GT5UDKD9YB6IO3A7WLNAAEHY0"
MY_ID = 1115358053
USER_FILE = "users.json"

def get_movies_from_google():
    # Target: Tomorrow's timings for LA Cinema Maris
    search_url = "https://www.google.com/search?q=LA+Cinema+Maris+Trichy+movie+timings+tomorrow"
    
    params = {
        'api_key': API_KEY,
        'url': search_url,
        'render_js': 'true',
        'premium_proxy': 'true',
        'country_code': 'in',
        'wait': '5000'
    }
    
    movie_results = []
    try:
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Google often lists timings in 'Vkp9Pc' or common snippets
            # Namma generic text search panni timings-ah filter pannuvom
            potential_blocks = soup.find_all(['div', 'span'])
            
            for block in potential_blocks:
                text = block.get_text(strip=True)
                # Looking for Movie titles and AM/PM timings
                if ("AM" in text or "PM" in text) and ":" in text:
                    if len(text) > 10 and len(text) < 200:
                        movie_results.append(f"🎬 {text}")
                        
        return list(dict.fromkeys(movie_results))[:12]
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []

def run_all():
    data = get_movies_from_google()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎥 *LA CINEMA (MARIS) - GOOGLE LIVE* 🎥\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Data not captured. Google might be showing a different layout."
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: Google Search Cache"
    final_msg = header + meta + body + footer

    # Broadcast to all users
    user_list = [MY_ID]
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                extra_users = json.load(f)
                for u in extra_users:
                    if u not in user_list: user_list.append(u)
            except: pass
            
    for user_id in user_list:
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={"chat_id": user_id, "text": final_msg, "parse_mode": "Markdown"})
        except: pass

if __name__ == "__main__":
    run_all()
