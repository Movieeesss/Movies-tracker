import requests
import json
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_data():
    # Direct BMS Theater API target (LA Cinemas Trichy code: LATG)
    # Intha URL direct-aa JSON data-va thara try pannum
    target_url = "https://in.bookmyshow.com/serv/getData?cmd=GETSHOWTIMESBYEVENT&f=json&dc=TRICH&vc=LATG&et=MT"
    
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in&render=true"
    
    movie_list = []
    try:
        response = requests.get(proxy_url, timeout=60)
        # Check if response is JSON
        try:
            data = response.json()
            # Inga BMS JSON structure-ah parse pannanum
            # Note: BMS API often changes, so we add a text-search backup
        except:
            # Fallback to direct page text search if JSON fails
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for all instances of "AM" and "PM" and their surrounding text
            import re
            text = soup.get_text()
            matches = re.findall(r'([A-Za-z0-9\s]+)\s+(\d{1,2}:\d{2}\s?(?:AM|PM))', text)
            for m in matches:
                movie_list.append({"name": m[0].strip(), "times": [m[1]]})
    except Exception as e:
        print(f"Error: {e}")
    
    return movie_list

def run_all():
    movies = get_movie_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Scraper Blocked / Data Hidden\n"
        msg += "⚠️ _BMS security is blocking the request._\n"
    else:
        # Grouping times by movie name
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Check BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
