import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_trichy_movies():
    target_url = "https://in.bookmyshow.com/explore/movies-trichy"
    
    # API Key illama scrap panna Headers romba mukkiyam
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    
    movie_list = set()
    try:
        # Direct-ah BookMyShow-ku request anupuroam
        response = requests.get(target_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Movie titles usually stay inside <h3> tags
            for h3 in soup.find_all('h3'):
                name = h3.get_text().strip().upper()
                if 3 < len(name) < 45:
                    if not any(x in name for x in ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER"]):
                        movie_list.add(name)
        else:
            print(f"BMS Blocked Us: Status {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return sorted(list(movie_list))

def run_all():
    movies = get_trichy_movies()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES LIST (FREE)* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "⚠️ *Status:* BMS blocked the Render server IP. API Key is needed for reliability.\n"
    else:
        body = "🎥 *NOW SHOWING:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    
    final_msg = header + meta + body + footer
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
