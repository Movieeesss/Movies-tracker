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

def get_bms_trichy_tomorrow_timings():
    # Specific URL for April 4, 2026 (Tomorrow)
    target_url = "https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404"
    
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true',
        'wait': '15000', # 15s wait for the green buttons to fully render
        'premium_proxy': 'true',
        'country_code': 'in'
    }
    
    movie_list = []
    try:
        # ScrapingBee API hit
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=70)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS tomorrow's page layout selection
            # 'list-item' is the standard row for each movie
            movie_rows = soup.select('.list-item') or soup.find_all('li', class_='list-item')
            
            for row in movie_rows:
                # Movie Name extraction
                title_tag = row.find('a', class_='__movie-name') or row.find('strong')
                if title_tag:
                    title = title_tag.get_text(strip=True).upper()
                    
                    # Showtimes extraction - specific targeting for the timing spans
                    time_tags = row.find_all(['div', 'span', 'a'], class_=re.compile(r'showtime|link|time'))
                    timings = []
                    for t in time_tags:
                        t_text = t.get_text(strip=True)
                        # Regular expression to catch 10:45 AM / 02:30 PM format
                        match = re.search(r'\d{1,2}:\d{2}\s?(?:AM|PM)?', t_text, re.I)
                        if match:
                            timings.append(match.group().strip())
                    
                    if title and timings:
                        # Sorting and unique timings
                        clean_times = " | ".join(sorted(list(set(timings))))
                        movie_list.append(f"🎬 *{title}*\n🕒 {clean_times}")
                        
        return movie_list
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_all():
    movies = get_bms_trichy_tomorrow_timings()
    
    # Time formatting for report
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎥 *LA CINEMA (MARIS) - TOMORROW (APR 4)* 🎥\n"
    meta = f"🕒 Report Generated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No timings found for tomorrow.\n_Reason: Bookings might not have opened or site is slow._"
    else:
        body = "\n\n".join(movies)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🎫 [Book Now on BMS](https://in.bookmyshow.com/cinemas/trichy/la-cinema-maris-trichy/buytickets/LATG/20260404)"
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
