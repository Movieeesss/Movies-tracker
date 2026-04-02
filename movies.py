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
    
    movie_list = set() 
    try:
        response = requests.get(proxy_url, timeout=35)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: BookMyShow movie titles usually inside <h3> or specific divs
            # H3 tags check panrom
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                
                # Filters: Ads and unwanted long sentences-ah skip panna
                if len(name) < 3 or len(name) > 45: continue
                if any(x in name for x in ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST"]): continue
                
                movie_list.add(name)

            # Method 2: Backup logic (Images-la irundhu title edukkurathu) 
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                blacklist = ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW", "OFFER", "STREAM", "OFFERS", "PROMO"]
                if not any(x in name for x in blacklist) and 3 < len(name) < 45:
                    if not any(x in name for x in ["BOOKING", "TICKET", "WATCH", "CLICK"]):
                        movie_list.add(name)
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* No movies detected. Check Proxy/API Key.\n"
    else:
        body = "🎥 *NOW SHOWING:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n" # Highlight illama normal format
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    
    final_msg = header + meta + body + footer
    # POST request use panrom for better reliability
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
