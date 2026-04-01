import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    # Wait time-ah 20s-ah fix pannitta output missing aagaathu
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=20000"
    
    movie_list = []
    try:
        response = requests.get(proxy_url, timeout=120)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Movie names posters-la irunthe edukkuroom (Kachithamaana vazhi)
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                if any(x in name for x in ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW"]):
                    continue
                if len(name) > 3 and name not in movie_list:
                    movie_list.append(name)
    except Exception as e:
        print(f"Error: {e}")
    return sorted(movie_list)

def run_all():
    # Start notification
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 *Scheduled Update: Checking Trichy Movies...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* Scraper busy or BMS load slow.\n"
    else:
        body = "🎥 *RECOMMENDED MOVIES:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-tiruchirappalli)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})
