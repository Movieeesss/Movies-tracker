import requests
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8529569809:AAFM-pmIKI5aVGvTSnGTr8ou9ogyAsus4VU"
API_KEY = "MKDCNDT9VWVFGX57CQ5NCR9R40F4FZWHDSLF98Z1KEK0NN5F9ZNKOM6GT5UDKD9YB6IO3A7WLNAAEHY0"
MY_ID = 1115358053
USER_FILE = "users.json"

def get_bms_tomorrow_heavy_mode():
    target_url = "https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404"
    
    # MAX POWER SETTINGS
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true',
        'wait': '30000',        # 30 SECONDS WAIT
        'premium_proxy': 'true', 
        'country_code': 'in'
    }
    
    movie_report = []
    try:
        # High timeout for heavy scraping
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=95)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('li', class_='list-item')
            
            for row in rows:
                title_tag = row.find('a', class_='__movie-name') or row.find('strong')
                if not title_tag: continue
                title = title_tag.get_text(strip=True).upper()
                
                # Extracting timings using text patterns
                raw_text = row.get_text(separator=" ", strip=True)
                timings = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM)?', raw_text, re.I)
                
                if title and timings:
                    unique_times = " | ".join(sorted(list(set(timings))))
                    movie_report.append(f"🎬 *{title}*\n🕒 {unique_times}")
                    
        return movie_report
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []

def run_all():
    data = get_bms_tomorrow_heavy_mode()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎥 *LA CINEMA (MARIS) - TOMORROW* 🎥\n"
    meta = f"🕒 Generated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No timings found.\n_Reason: Site rendering took too long._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🎫 Book: [lacucinema.com](https://www.lacucinema.com/)"
    final_msg = header + meta + body + footer

    # Send to users
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
