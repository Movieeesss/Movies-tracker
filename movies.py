import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # Direct URL for April 2nd
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
    
    # 15 seconds wait kuduthuruken for heavy dynamic loading
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=180)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- BROAD SCAN LOGIC ---
            # Search every list item and div that could be a movie block
            containers = soup.find_all(['li', 'div'], class_=re.compile(r'list|card|listing|info', re.I))
            
            for container in containers:
                # Name search
                name_tag = container.find(attrs={"data-event-title": True})
                if name_tag:
                    name = name_tag['data-event-title']
                else:
                    name_tag = container.select_one('.movie-name, .name, strong, h5')
                    name = name_tag.get_text(strip=True) if name_tag else ""

                # Timings search (Regex pattern for 10:30 AM/PM)
                content = container.get_text(separator=' ', strip=True)
                times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?', content)
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})

    except Exception as e:
        print(f"Scrape Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    
    msg = f"🎬 *LA CINEMAS (MARIS) - THU 02 APR* 🎬\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Waiting for BMS Timings... 🕒\n"
        msg += "💡 _Timing extraction failed. Retrying..._\n"
    else:
        # Removing duplicates and 'Movie Found' type entries
        final_list = {}
        for m in movies:
            if len(m['name']) > 2 and len(m['times']) > 0:
                final_list[m['name'].upper()] = m['times']
        
        for name, times in final_list.items():
            msg += f"🎥 *{name}*\n🕒 {', '.join(times)}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
