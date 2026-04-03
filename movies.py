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

def get_bms_trichy_timings():
    # Direct BMS URL for LA Cinema Maris
    target_url = "https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404"
    
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true',
        'wait': '12000', # BMS load aaga 12s wait pannanum
        'premium_proxy': 'true'
    }
    
    movie_list = []
    try:
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS layout-la 'list-item' thaan ovvoru movie row
            movie_containers = soup.select('.list-item') or soup.find_all('li', class_='list-item')
            
            for container in movie_containers:
                # Movie Name
                title_tag = container.find('a', class_='__movie-name')
                if title_tag:
                    title = title_tag.get_text(strip=True).upper()
                    
                    # Showtimes - Intha green buttons kulla irukura timings
                    time_tags = container.find_all('div', class_='__showtime-link')
                    timings = []
                    for t in time_tags:
                        # Extracting 10:40 AM maari irukura text
                        t_text = t.get_text(strip=True)
                        # Cleaning: "10:40 AM DOLBY ATMOS" -> "10:40 AM"
                        clean_time = re.search(r'\d{1,2}:\d{2}\s?(?:AM|PM)?', t_text, re.I)
                        if clean_time:
                            timings.append(clean_time.group().strip())
                    
                    if title and timings:
                        time_display = " | ".join(timings)
                        movie_list.append(f"🎬 *{title}*\n🕒 {time_display}")
                        
        return movie_list
    except Exception as e:
        print(f"BMS Error: {e}")
        return []

def run_all():
    movies = get_bms_trichy_timings()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎥 *LA CINEMA (MARIS) - LIVE SHOWS* 🎥\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No timings found.\n_Wait time increase panni check pannanum._"
    else:
        body = "\n\n".join(movies)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🎫 [Book on BMS](https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404)"
    final_msg = header + meta + body + footer

    # Broadcasting to users
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
