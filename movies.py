import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_live_timings():
    # Targeted Search for LA Cinemas Maris Trichy Showtimes
    query = "LA+Cinemas+Maris+Trichy+show+timings+today"
    target_url = f"https://www.google.com/search?q={query}&hl=en"
    
    # Using ScraperAPI with India Proxy + JS Rendering to see what a human sees
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in&render=true"
    
    movie_list = []
    try:
        response = requests.get(proxy_url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google search results cards find panrom
        # 'div' with specific data-attrid contains the movie info
        containers = soup.find_all('div', attrs={'data-attrid': re.compile(r'kc:/film/film:showtimes')})
        
        for container in containers:
            name = container.find('div', class_='BNeaW').get_text() if container.find('div', class_='BNeaW') else "Movie"
            # Find all showtime patterns (e.g., 10:30 AM, 2:45 PM, 10:15 PM)
            all_text = container.get_text()
            times = re.findall(r'\d{1,2}:\d{2}\s?[APM]{2}', all_text)
            
            if times:
                movie_list.append({"name": name, "times": list(dict.fromkeys(times))})

        # Fallback: If containers fail, search all text for timings
        if not movie_list:
            full_text = soup.get_text()
            # Regex: Finds any time format 00:00 AM/PM
            raw_times = re.findall(r'\d{1,2}:\d{2}\s?[APM]{2}', full_text)
            if raw_times:
                movie_list.append({"name": "Current Movies", "times": list(dict.fromkeys(raw_times))})

    except Exception as e:
        print(f"Bypass Error: {e}")
    
    return movie_list

def run_all():
    movies = get_live_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Scraper bypassing security...\n"
        msg += "⚠️ _Google is refreshing data. Retry in 5 mins._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
