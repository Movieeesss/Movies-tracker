import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # April 2nd target
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
    
    # Increase timeout and wait for the main list container
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait_for=#venuelist&wait=20000"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=210)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # METHOD 1: Look for individual movie entries (Latest BMS Classes)
            # BMS ippo 'listing-info' or 'list' use panraanga
            items = soup.select('li.list, .listing-info, .venue-listing-item')
            
            for item in items:
                # Movie Name - usually inside strong or data attributes
                name_tag = item.find('strong') or item.select_one('.movie-name')
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                # Showtimes - looking for pills/session times
                time_tags = item.find_all('div', {'class': re.compile(r'showtime|pill|session', re.I)})
                # If div not found, try 'a' tags
                if not time_tags:
                    time_tags = item.find_all('a', {'data-session-id': True})
                
                times = []
                for t in time_tags:
                    t_text = t.get_text(strip=True)
                    # Cleaning time format (e.g., 10:30 AM)
                    time_match = re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)?', t_text, re.I)
                    if time_match:
                        times.append(time_match.group())

                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})

            # METHOD 2: Backup - Scrape from Script tag (Structured Data)
            if not movie_results:
                script_tag = soup.find('script', type='application/ld+json')
                if script_tag:
                    data = json.loads(script_tag.string)
                    # Structured data analysis logic inge varum (if needed)

    except Exception as e:
        print(f"Scraping Error: {e}")
    
    return movie_results

def run_all():
    movies_list = get_movie_timings()
    # Correcting IST Time
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    meta = f"📅 *DATE:* 02-04-2026\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies_list:
        body = "📊 *Status:* Theater syncing live timings...\n"
        body += "💡 _BMS security is high. Retrying in next cycle._\n"
    else:
        body = ""
        for m in movies_list:
            body += f"🎥 *{m['name'].upper()}*\n🕒 {', '.join(m['times'])}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    
    full_msg = header + meta + body + footer
    
    # Telegram Send
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": full_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
