import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    # 10 seconds wait kuduthurukken timings full-aa load aaga
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=150)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS layout-la 'li.list' dhaan ovvoru movie block
            containers = soup.select('li.list')
            
            for container in containers:
                # 1. Movie Name accurate-aa edukka (BMS uses 'data-event-title' or '.name' class)
                name_tag = container.find(attrs={"data-event-title": True})
                if name_tag:
                    name = name_tag['data-event-title']
                else:
                    name_tag = container.select_one('.movie-name, .name, strong')
                    name = name_tag.get_text(strip=True) if name_tag else ""

                # 2. Timings accurate-aa edukka
                # Scraper page-la irukra timings pills-ah theidum
                time_tags = container.find_all('a', class_=re.compile(r'showtime|pill|session|time', re.I))
                times = []
                for t in time_tags:
                    t_text = t.get_text(strip=True)
                    if re.search(r'\d{1,2}:\d{2}', t_text):
                        # Cleaning times (Removing 'INFO' or other extra text if any)
                        clean_time = re.search(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?', t_text)
                        if clean_time:
                            times.append(clean_time.group())
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})

    except Exception as e:
        print(f"Bypass Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - MASTER UPDATES* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* No shows found for today/tomorrow.\n"
        msg += "💡 _Check if bookings are open on BMS site._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name'].upper()}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
