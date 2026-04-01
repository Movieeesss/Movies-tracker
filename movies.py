import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Bot Settings
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "f1616ee794ad045c5d214aba40fda508"

def get_trichy_movies():
    # Trichy movies exploration page
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    
    # Render=true kudutha thaan antha movie cards load aagum
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    movie_list = []
    try:
        print("Fetching Trichy movie listings...")
        response = requests.get(proxy_url, timeout=180)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS layout-la movie title intha class patterns-la thaan irukkum
            # Neenga screenshot-la kaatuna Youth, Happy Raj ellaathaiyum ithu filter pannum
            title_elements = soup.find_all(['div', 'title'], class_=re.compile(r'CardTitle|Title', re.I))
            
            for elem in title_elements:
                name = elem.get_text(strip=True).upper()
                # Dummy values or too short names-ah filter panrom
                if len(name) > 2 and name not in movie_list:
                    movie_list.append(name)
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Scraping Error: {e}")
        
    return movie_list

def run_all():
    # Progress alert
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔎 *Scanning Trichy Recommended Movies...*", "parse_mode": "Markdown"})
    
    movies = get_trichy_movies()
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* No movies found. Page might be loading slow.\n"
        body += "💡 _Check your API limits or Wait time._\n"
    else:
        body = "🎥 *RECOMMENDED MOVIES:*\n\n"
        for m in movies:
            # Ippo list-la ulla ella movie names-um varum
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Check on BMS](https://in.bookmyshow.com/explore/home/trichy)"
    
    # Final message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
