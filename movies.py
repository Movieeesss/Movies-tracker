import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_la_cinemas_live_data():
    # April 03 date-ah dynamic-ah calculate panrom
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    # If it's already April 03, use today. If not, use tomorrow.
    check_date = ist_now if ist_now.day == 3 else (ist_now + timedelta(days=1))
    date_str = check_date.strftime("%Y%m%d")
    
    # Strictly LATG-MT URL
    target_url = f"https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LATG-MT/{date_str}"
    
    # Proxy-la innum nalla wait time (20s) tharom to load full content
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=20000"
    
    theater_data = {}
    try:
        response = requests.get(proxy_url, timeout=90)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS theater page structure loop
            movie_elements = soup.select('li.list')
            
            for movie in movie_elements:
                # Movie name search
                name_tag = movie.find('a', class_='__movie-name')
                if not name_tag: continue
                movie_name = name_tag.get_text().strip().upper()
                
                # Live timings search
                timings = []
                # Timings are usually in 'showtime-pill' or anchor tags with session links
                time_tags = movie.select('.showtime-pill, .__showtime, a[data-session-id]')
                
                for t in time_tags:
                    time_val = t.get_text().strip()
                    # Filter for valid time formats like 11:00 AM
                    if ":" in time_val and any(c.isdigit() for c in time_val):
                        # Cleaning (Removing Dolby/4K info)
                        clean_time = time_val.split('\n')[0].strip()
                        if clean_time not in timings:
                            timings.append(clean_time)
                
                if movie_name and timings:
                    theater_data[movie_name] = timings
        else:
            print(f"Scraper Status Error: {response.status_code}")
    except Exception as e:
        print(f"Scraping Exception: {e}")
        
    return theater_data, date_str

def run_all():
    data, date_val = get_la_cinemas_live_data()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    display_date = datetime.strptime(date_val, "%Y%m%d").strftime("%d-%b")
    
    header = f"🍿 *LA CINEMA - {display_date} LIVE UPDATES* 🍿\n"
    meta = f"🕒 Check Time: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = f"⚠️ *Status:* No shows found in the live scan for {display_date}. Website may be blocking or page changed."
    else:
        body = "🎥 *CURRENT SHOWS & TIMINGS:*\n\n"
        for movie, times in data.items():
            body += f"✅ *{movie}*\n"
            body += f"🕒 {' | '.join(times)}\n\n"
            
    footer = f"━━━━━━━━━━━━━━━━━━━━\n👉 [Live Booking Link](https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LATG-MT/{date_val})"
    
    final_msg = header + meta + body + footer
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
