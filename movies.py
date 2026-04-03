import requests
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
API_KEY = "MKDCNDT9VWVFGX57CQ5NCR9R40F4FZWHDSLF98Z1KEK0NN5F9ZNKOM6GT5UDKD9YB6IO3A7WLNAAEHY0"
USER_FILE = "users.json"
MY_ID = 1115358053  

def get_bms_tomorrow_pakkava_timings():
    # April 4 tomorrow link
    target_url = "https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404"
    
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true',
        'wait': '20000', # 20s wait! Full-ah render aana thaan timings kidaikum
        'premium_proxy': 'true'
    }
    
    movie_report = []
    try:
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=80)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS tomorrow page-la ovvoru movie row-vum 'list-item' class-la irukkum
            rows = soup.find_all('li', class_='list-item')
            
            for row in rows:
                # 1. Movie Name target
                title_tag = row.find('a', class_='__movie-name')
                if not title_tag: continue
                title = title_tag.get_text(strip=True).upper()
                
                # 2. Timings target (Finding all spans with time pattern)
                # Regex looks for 10:45 AM, 02:30 PM etc.
                raw_text = row.get_text(separator=" ", strip=True)
                timings = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM)?', raw_text, re.I)
                
                if title and timings:
                    # Remove duplicates and clean
                    unique_times = " | ".join(sorted(list(set(timings))))
                    movie_report.append(f"🎬 *{title}*\n🕒 {unique_times}")
                    
        return movie_report
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []

def run_all():
    # Calling the new scrapper
    movies = get_bms_tomorrow_pakkava_timings()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎥 *LA CINEMA (MARIS) - TOMORROW (APR 4)* 🎥\n"
    meta = f"🕒 Generated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No timings detected yet.\n_Reason: Site rendering slow or Booking not open._"
    else:
        body = "\n\n".join(movies)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🎫 [Book Online](https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404)"
    final_msg = header + meta + body + footer

    # Broadcast logic
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
                          data={"chat_id": user_id, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})
        except: pass

if __name__ == "__main__":
    run_all()
