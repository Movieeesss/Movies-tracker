import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
# Unga puthu API Key
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_movie_timings():
    # Direct BMS Theater Page (LA Cinemas Maris)
    target_url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    
    # WebScraping.ai API Logic:
    # proxy=residential (Idhu thaan normal mobile/home network maadhiri kaattum)
    # render=true (JavaScript-ah load panni timings-ah veliya kondu varum)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true"
    
    movie_results = []
    try:
        # 60 seconds timeout kuduthurukkaam, ஏன்னா residential proxy konjam slow-aa dhaan load aagum
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS New Layout scan: Movies are usually in <li> tags with class 'list'
            movie_blocks = soup.find_all('li', class_='list')
            
            # Layout fallback: If <li> not found, search for common movie title classes
            if not movie_blocks:
                movie_blocks = soup.select('.listing-info')

            for block in movie_blocks:
                # Extract Movie Name
                name_tag = block.find('strong') or block.select_one('.movie-name')
                name = name_tag.get_text(strip=True) if name_tag else ""
                
                # Extract Timings (Showtime pills)
                time_tags = block.find_all('a', class_='showtime-pill')
                times = [t.get_text(strip=True) for t in time_tags if ":" in t.get_text()]
                
                if name and times:
                    movie_results.append({"name": name, "times": times})
                    
    except Exception as e:
        print(f"Bypass Error: {e}")
    
    return movie_results

def run_all():
    movies = get_movie_timings()
    
    # IST Time Calculation
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - MASTER UPDATES* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater syncing live timings...\n"
        msg += "⚠️ _Security is high today. Retrying via Residential Proxy._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Book on BookMyShow](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    # Sending to Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    run_all()
