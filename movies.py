import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Bot Settings
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "f1616ee794ad045c5d214aba40fda508"

def get_trichy_movies():
    # Direct Trichy Movies Page
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    
    # Render=true + 20s wait (BMS cards load aaga Render-ku ivvalo neram venum)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=20000"
    
    movie_list = []
    try:
        print("Connecting to BMS via API...")
        response = requests.get(proxy_url, timeout=180)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: Image Alt Tags (Most Stable)
            # Movie posters-oda alt text-la nichayam movie name irukkum
            images = soup.find_all('img', alt=True)
            for img in images:
                name = img['alt'].strip().upper()
                # Unwanted labels-ah filter panrom
                if any(x in name for x in ["BMS", "LOGO", "BANNER", "APP", "BOOKMYSHOW", "OFFER", "STREAM"]):
                    continue
                if len(name) > 3 and name not in movie_list:
                    movie_list.append(name)
            
            # Method 2: Fallback to Card Titles
            if not movie_list:
                titles = soup.find_all(['div', 'strong'], class_=re.compile(r'CardTitle|Title', re.I))
                for t in titles:
                    name = t.get_text(strip=True).upper()
                    if len(name) > 3 and name not in movie_list:
                        movie_list.append(name)
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Scraping Error: {e}")
        
    return sorted(movie_list)

def run_all():
    # Immediate Start Message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔄 *2-Hour Scheduled Scan: Fetching Trichy Movies...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES UPDATE* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* No movies found in this cycle.\n"
        body += "💡 _Check if API credits are exhausted or BMS layout changed._\n"
    else:
        body = "🎥 *MOVIES CURRENTLY LISTED:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BookMyShow](https://in.bookmyshow.com/explore/movies-tiruchirappalli)\nNext update in 2 hours."
    
    # Final Send
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
