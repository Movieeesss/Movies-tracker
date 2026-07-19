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
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    # Using stealth proxy to avoid Cloudflare blocks
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=stealth&render=true&wait=10000"
    
    raw_movies = set()
    final_movies = set()
    
    try:
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by BookMyShow Anti-bot (Cloudflare).")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # STRATEGY 1: Find movie names from image 'alt' tags inside movie links (Most reliable for BMS)
            for a in soup.find_all('a', href=True):
                if '/movies/' in a['href'] and 'ET00' in a['href']:
                    img = a.find('img')
                    if img and img.get('alt'):
                        raw_movies.add(img.get('alt').strip().upper())
            
            # STRATEGY 2: Fallback to h3 tags just in case
            for h3 in soup.find_all('h3'):
                raw_movies.add(h3.get_text().strip().upper())
                
            # STRATEGY 3: Fallback to prominent divs inside movie links
            for a in soup.find_all('a', href=True):
                if '/movies/' in a['href'] and 'ET00' in a['href']:
                    texts = [div.get_text().strip().upper() for div in a.find_all('div') if div.get_text().strip()]
                    if texts:
                        raw_movies.add(texts[0]) # Usually the first text is the title

            # Filter and clean the scraped list
            blacklist = ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST", "BMS", "SCREEN", "PROMOTED", "ADVERTISEMENT", "RUPEES"]
            
            for name in raw_movies:
                if 2 < len(name) < 50:
                    if not any(x in name for x in blacklist):
                        final_movies.add(name)
                        
            if not final_movies:
                print("⚠️ WARNING: Page loaded, but no movie names could be extracted. DOM might be completely different.")
                
        else:
            print(f"⚠️ Scraper Error: HTTP Status Code {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Network/Scraper Error: {e}")
        
    return sorted(list(final_movies))

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
