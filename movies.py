import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    # Residential Proxy + JS Rendering for maximum bypass
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # BMS layout: movies are usually in <li> with class 'list'
            movie_blocks = soup.find_all('li', class_='list')
            
            for block in movie_blocks:
                name_tag = block.find('strong')
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                time_tags = block.find_all('a', class_='showtime-pill')
                times = [t.get_text(strip=True) for t in time_tags if ":" in t.get_text()]
                
                if name and times:
                    movie_results.append({"name": name, "times": times})
    except Exception as e:
        print(f"Scrape Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Syncing theater timings...\n⚠️ _BMS security is high today._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
