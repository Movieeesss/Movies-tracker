import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # Adding wait=10000 (10 seconds) for the heaviest layout loading
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=150)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- ULTIMATE TEXT SCAN ---
            # Finding all blocks that look like a movie entry
            blocks = soup.find_all(['li', 'div'], class_=re.compile(r'list|card|listing|container', re.I))
            
            for block in blocks:
                # Text content of the entire block
                content = block.get_text(separator=' ', strip=True)
                
                # Regex for Movie Name (Looking for capitalized words at start)
                # Regex for Time (10:30 AM/PM style)
                times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)', content)
                
                if times:
                    # Trying to find the most likely title in that block
                    # Usually titles are in <strong> or <h5>
                    title_tag = block.find(['strong', 'h5', 'span'], class_=re.compile(r'name|title|Event', re.I))
                    title = title_tag.get_text(strip=True) if title_tag else "Movie Found"
                    
                    movie_results.append({"name": title, "times": list(dict.fromkeys(times))})

            # Deep Fallback: If nothing found, scan the WHOLE PAGE for any time patterns
            if not movie_results:
                full_text = soup.get_text(separator=' ')
                all_times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)', full_text)
                if all_times:
                    movie_results.append({"name": "Live Movies", "times": list(dict.fromkeys(all_times))})

    except Exception as e:
        print(f"Scrape Error: {e}")
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* BMS Security blocked deep-scan.\n"
        msg += "💡 _Timing extraction failed. Retrying in next cycle._\n"
    else:
        # Removing duplicates
        unique_movies = {m['name']: m['times'] for m in movies if m['name'] != "Movie Found"}
        if not unique_movies: # Fallback display
             for m in movies: msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
        else:
            for name, times in unique_movies.items():
                msg += f"🎥 *{name}*\n🕒 {', '.join(times)}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
