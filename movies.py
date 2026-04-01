import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
    
    # Wait time-ah 20 seconds-ah increase pannittom (Render speed-ku safe)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=20000"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=150)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS layout-la ellamae 'li' tags kulla thaan irukkum
            items = soup.find_all('li', class_=re.compile(r'list|listing', re.I))
            
            for item in items:
                # Movie Name search (BMS ippo 'strong' use panraanga)
                name_tag = item.find('strong') or item.find('span', class_=re.compile(r'name|title', re.I))
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                # Showtimes search (Looking for AM/PM patterns)
                # Ithu direct-ah text-laye filter panni timing-ah eduthudum
                raw_text = item.get_text(" ", strip=True)
                time_strings = re.findall(r'\d{1,2}:\d{2}\s*(?:AM|PM)?', raw_text, re.I)
                
                if name and time_strings:
                    clean_times = sorted(list(set(time_strings)))
                    movie_results.append({"name": name.upper(), "times": clean_times})
                    
    except Exception as e:
        print(f"Error: {e}")
    return movie_results

def run_all():
    # First confirmation message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 Checking LA Cinemas (Maris)... Please wait 30s.", "parse_mode": "Markdown"})
    
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    meta = f"📅 *DATE:* 02-04-2026\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* Theater syncing live timings...\n"
        body += "💡 _Try checking the BMS link manually for a moment._\n"
    else:
        body = ""
        for m in movies:
            body += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
