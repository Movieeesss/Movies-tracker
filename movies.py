import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def deep_scrape_bms():
    # Direct BMS Theater Link - Most accurate source
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    
    # POWERFUL PARAMS: 
    # render=true (JS load pannum)
    # country_code=in (India IP)
    # wait_until=networkidle (Full-aa load aagura varai wait pannum)
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in&render=true&wait_until=networkidle"
    
    movie_results = []
    
    # RETRY LOGIC: Oru vaati fail aana thirumbavum 3 times try pannum
    for attempt in range(3):
        try:
            print(f"Attempt {attempt+1}: Scraping BMS...")
            response = requests.get(proxy_url, timeout=90)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # BMS New Layout Logic:
                # Movies usually in containers with 'listing-info' or 'movie-card'
                movie_containers = soup.find_all('li', class_='list') or soup.select('.listing-info')
                
                for container in movie_containers:
                    # Extract Movie Name
                    name_tag = container.find('strong') or container.select_one('.movie-name')
                    name = name_tag.get_text(strip=True) if name_tag else ""
                    
                    # Extract All Showtimes for that movie
                    time_tags = container.find_all('a', class_='showtime-pill') or container.select('.showtime-pill')
                    times = [t.get_text(strip=True) for t in time_tags if ":" in t.get_text()]
                    
                    if name and times:
                        movie_results.append({"name": name, "times": times})
                
                if movie_results:
                    break # Success! Loop-ah vittu veliya vandhurum
            
            time.sleep(5) # Fail aana 5 seconds gap vittu thirumba try pannum
        except Exception as e:
            print(f"Error on attempt {attempt+1}: {e}")
            
    return movie_results

def run_all():
    movies = deep_scrape_bms()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🏗️ *ULTIMATE MOVIE TRACKER - LIVE* 🏗️\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "⚠️ *Status:* BMS Security is high today.\n"
        msg += "📊 *Action:* Retrying via Cron-job soon...\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Direct Booking Link](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    run_all()
