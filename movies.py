import requests
import re
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_data():
    # Targeted BMS Search API for LA Cinemas Maris (LATG)
    target_url = "https://in.bookmyshow.com/serv/getData?cmd=GETSHOWTIMESBYEVENT&f=json&dc=TRICH&vc=LATG"
    
    # Using ScraperAPI with India Proxy
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=60)
        
        # Method 1: Try parsing as JSON (Direct API)
        try:
            data = response.json()
            if 'BookMyShow' in data and 'arrEvents' in data['BookMyShow']:
                events = data['BookMyShow']['arrEvents']
                for event in events:
                    name = event.get('EventName', 'Movie')
                    # Find timings in the child objects
                    times = [] # Add logic to extract times from child arrays if present
                    if name:
                        movie_results.append({"name": name, "times": ["Check BMS for times"]})
        except:
            # Method 2: If JSON fails, deep search text for time patterns
            text = response.text
            # Finds patterns like 10:30 AM, 02:15 PM
            raw_times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)', text)
            if raw_times:
                movie_results.append({"name": "Current Shows", "times": list(dict.fromkeys(raw_times))})

    except Exception as e:
        print(f"API Error: {e}")
    
    return movie_results

def run_all():
    movies = get_movie_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "⚠️ *Status:* BMS Security Blocked / No Data Found.\n"
        msg += "💡 _Possible reason: ScraperAPI Credits exhausted or IP block._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
