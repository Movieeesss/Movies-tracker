import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=75) # Increased timeout
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- NEW POWERFUL SELECTOR ---
            # Movie cards usually have 'listing-info' or 'movie-card' classes
            containers = soup.select('.listing-info, .movie-card, li.list')
            
            for container in containers:
                # Find Movie Name (Strong tags or specific classes)
                name_tag = container.find(['strong', 'h5']) or container.select_one('.movie-name, .name')
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                # Find Timings (Anything with a colon and AM/PM or just numbers in pills)
                time_tags = container.find_all('a', class_=re.compile(r'showtime|pill|session'))
                times = [t.get_text(strip=True) for t in time_tags if re.search(r'\d{1,2}:\d{2}', t.get_text())]
                
                if name and times:
                    movie_results.append({"name": name, "times": list(dict.fromkeys(times))})
            
            # Fallback: If containers fail, do a deep text scan
            if not movie_results:
                text_data = soup.get_text()
                # Find patterns like "Movie Name 10:30 AM"
                # This is a bit complex, so we prioritize the above selectors first.
                pass

    except Exception as e:
        print(f"Bypass Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater syncing live timings...\n"
        msg += "⚠️ _Check manual link below for now._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
