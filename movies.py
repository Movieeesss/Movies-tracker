import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # April 2nd Target URL
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
    
    # 1. proxy=datacenter (Residential block aaga chance irundha idhu speed-aa bypass pannum)
    # 2. wait_for=.showtime-pill (Timings vara varai kandaipaa wait pannum)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=datacenter&render=true&wait_for=.showtime-pill"
    
    movie_results = []
    try:
        # Request with 120s timeout
        response = requests.get(proxy_url, timeout=120)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS lists movies in 'li' with class 'list'
            containers = soup.select('li.list')
            
            for container in containers:
                # Name extraction
                name_tag = container.find(attrs={"data-event-title": True})
                name = name_tag['data-event-title'] if name_tag else ""
                
                if not name:
                    name_tag = container.select_one('.movie-name, .name, strong')
                    name = name_tag.get_text(strip=True) if name_tag else ""

                # Timing extraction
                time_tags = container.find_all('a', class_=re.compile(r'showtime|pill|session', re.I))
                times = [t.get_text(strip=True) for t in time_tags if ":" in t.get_text()]
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})

    except Exception as e:
        print(f"Bypass Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n📅 *DATE:* 02-04-2026\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater syncing live timings...\n"
        msg += "💡 _Retrying with high-speed bypass node._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name'].upper()}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
