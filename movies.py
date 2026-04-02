import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_trichy_movies():
    # Corrected URL for Trichy
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    
    # CRITICAL FIX: Wait time changed from 20000 to 10000 to fit Cron-job.org's 30s limit
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_list = []
    try:
        # Timeout set to 25s so it fails internally before Cron-job kills it at 30s
        response = requests.get(proxy_url, timeout=25)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract movie names from image alt tags
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                # Advanced filtering to remove noise
                if any(x in name for x in ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW", "OFFER", "STREAM", "PROMO"]):
                    continue
                if len(name) > 3 and name not in movie_list:
                    movie_list.append(name)
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(movie_list)

def run_all():
    # 1. Notify start (Optional, but useful to know the script is alive)
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 *Checking Trichy Movies...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    
    # IST Time calculation
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* No movies found. (Could be a slow proxy or page layout change).\n"
    else:
        body = "🎥 *RECOMMENDED MOVIES:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-tiruchirappalli)"
    
    # 2. Send the final list to Telegram
    final_msg = header + meta + body + footer
    tg_response = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                               params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

    # --- FINAL CLEANUP FOR CRON-JOB.ORG ---
    # We print only a tiny string to keep output size small
    if tg_response.status_code == 200:
        print("Success: Telegram notification sent.")
    else:
        print(f"Failed: Telegram status {tg_response.status_code}")

if __name__ == "__main__":
    run_all()
