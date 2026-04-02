import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    # WebScraping.AI settings
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=20000"
    
    movie_list = []
    try:
        # Timeout 120s kuduthurukkom because wait=20s + rendering time edukum
        response = requests.get(proxy_url, timeout=150)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Movie names posters-la irunthe edukkuroom
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                # Filtering useless tags
                if any(x in name for x in ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW", "OFFER", "STREAM"]):
                    continue
                if len(name) > 3 and name not in movie_list:
                    movie_list.append(name)
        else:
            # Error vantha verum status code mattum print aagum (Not full HTML)
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(movie_list)

def run_all():
    # 1. Start Notification
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 *Checking Trichy Movies...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    
    # Time logic updated for latest Python versions
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* Movies list empty. Scraper busy or page not loaded properly.\n"
    else:
        body = "🎥 *RECOMMENDED MOVIES:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-tiruchirappalli)"
    
    # 2. Final Telegram message
    final_msg = header + meta + body + footer
    tg_response = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                               params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

    # --- CRITICAL FIX FOR CRON-JOB.ORG ---
    # Inga periya string ethaiyume print panna koodathu
    if tg_response.status_code == 200:
        print("Success: Telegram notification sent.")
    else:
        print(f"Failed: Telegram status {tg_response.status_code}")

if __name__ == "__main__":
    run_all()
