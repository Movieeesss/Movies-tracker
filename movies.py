import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- NEW BOT CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_la_maris_shows():
    # Today's date in YYYYMMDD format
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    
    # Live URL for LA Maris Trichy
    url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{date_str}"
    
 headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://in.bookmyshow.com/trichy',
        'Connection': 'keep-alive'
    }
    
    movie_list = []
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BMS listings focus
        listings = soup.find_all('li', class_='list')
        
        for item in listings:
            # Get Movie Title
            title_tag = item.find('strong')
            if title_tag:
                name = title_tag.text.strip()
                
                # Get Show Timings
                times = []
                details = item.find_all('div', class_='__details')
                for d in details:
                    # Filter out just the time (e.g., 10:30 AM)
                    t_text = d.text.strip().split('\n')[0]
                    if ":" in t_text:
                        times.append(t_text)
                
                if name and times:
                    movie_list.append({"name": name, "times": times})
        
        return movie_list
    except Exception as e:
        print(f"Scrape Error: {e}")
        return []

def send_to_telegram():
    movies = get_la_maris_shows()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    if not movies:
        # Static Fallback if BMS blocks the request
        msg = "🎬 *LA CINEMAS (MARIS) - TRICHY*\n"
        msg += "⚠️ Live data update failed. Please check BMS website directly."
    else:
        msg = f"🎬 *LA CINEMAS (MARIS) - SHOWS*\n"
        msg += f"📅 {today}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        for m in movies:
            msg += f"🎥 *{m['name']}*\n"
            msg += f"🕒 {', '.join(m['times'])}\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        msg += "🎟️ [Book on BookMyShow](https://in.bookmyshow.com/trichy/cinemas/la-cinemas-maris-trichy/LATG)"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True}
    requests.get(url, params=payload)

if __name__ == "__main__":
    send_to_telegram()
