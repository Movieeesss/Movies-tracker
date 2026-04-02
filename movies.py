import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    
    # render=true koodave wait time 10s kuduthurukom, so page nalla load aagum
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movie_list = set() # Duplicate thavirkka set use pandrom
    try:
        response = requests.get(proxy_url, timeout=28)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: BookMyShow-oda common movie title class/structure
            # Intha div-kulla dhaan title irukkum
            for div in soup.find_all('div', attrs={'style': lambda x: x and 'color: rgb(34, 34, 34)' in x}):
                name = div.get_text().strip().upper()
                if len(name) > 2:
                    movie_list.add(name)

            # Method 2: Backup logic (Images-la irundhu title edukkurathu)
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                # Unwanted items-ah mattum filter pandrom
                blacklist = ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW", "OFFER", "STREAM"]
                if not any(x in name for x in blacklist):
                    if len(name) > 3:
                        movie_list.add(name)
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    # Progress alert (optional)
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 *Fetching All Movies (Including Happy Raj)...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No movies detected. Check Proxy/API Key.\n"
    else:
        body = "🎥 *CURRENTLY SHOWING:*\n\n"
        for m in movies:
            # Special emoji for "HAPPY RAJ" if found
            emoji = "🌟" if "HAPPY RAJ" in m else "✅"
            body += f"{emoji} *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

    print("Process Completed.")

if __name__ == "__main__":
    run_all()
