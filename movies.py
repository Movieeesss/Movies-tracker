import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # April 2nd Page URL
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
    
    # wait_for=.showtime-pill makes the scraper wait until the actual timing pills appear on screen
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait_for=.showtime-pill&timeout=30000"
    
    movie_results = []
    try:
        # Long timeout because residential + waiting for element is slow
        response = requests.get(proxy_url, timeout=180)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Finding movie blocks (li.list is the standard BMS block)
            containers = soup.select('li.list, .movie-card, .listing-info')
            
            for container in containers:
                # Precise name extraction
                name_tag = container.find(attrs={"data-event-title": True})
                if name_tag:
                    name = name_tag['data-event-title']
                else:
                    name_tag = container.select_one('.movie-name, .name, strong')
                    name = name_tag.get_text(strip=True) if name_tag else ""

                # Precise timing extraction
                time_tags = container.find_all('a', class_=re.compile(r'showtime|pill|session|time', re.I))
                times = [t.get_text(strip=True) for t in time_tags if re.search(r'\d{1,2}:\d{2}', t.get_text())]
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})

    except Exception as e:
        print(f"Bypass Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    
    msg = f"🎬 *LA CINEMAS (MARIS) - THU 02 APR* 🎬\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Data Hidden by BMS Script.\n"
        msg += "💡 _Retrying with extended bypass logic..._\n"
    else:
        # Displaying with proper formatting
        for m in movies:
            msg += f"🎥 *{m['name'].upper()}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
