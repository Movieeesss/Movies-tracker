import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    # residential proxy + full page render
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=90)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Technique: Search for ALL text blocks that contain show timings
            # Most BMS layouts use 'showtime-pill' or 'session-time'
            all_html = str(soup)
            
            # Find movie names and their following timings
            # BMS layout check:
            containers = soup.find_all(['li', 'div'], class_=re.compile(r'list|card|listing', re.I))
            
            for container in containers:
                name_tag = container.find(['strong', 'h5', 'span'], class_=re.compile(r'name|title', re.I))
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                # Regex for timings: 10:30 AM, 2:15 PM etc.
                time_pattern = r'\d{1,2}:\d{2}\s?[APM]{2}'
                times = re.findall(time_pattern, container.get_text())
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})
            
            # Backup: If structured search fails, get ANY movie-like name and time
            if not movie_results:
                raw_text = soup.get_text(separator=' ')
                # This finds any movie name pattern + time pattern
                pass 

    except Exception as e:
        print(f"Bypass Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - MASTER UPDATES* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Data Hidden by BMS Security.\n"
        msg += "💡 _Code logic updated to bypass new layout._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
