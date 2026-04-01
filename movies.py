import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def run_all():
    # India IP (Render Singapore) nala ippo direct BMS try pannuvom with better headers
    url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260401"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    movie_list = []
    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # BMS-oda latest class patterns
        for item in soup.find_all('li', class_='list'):
            name = item.find('strong').text.strip() if item.find('strong') else ""
            times = [t.text.strip() for t in item.find_all('div', class_='__details') if ":" in t.text]
            if name and times:
                movie_list.append({"name": name, "times": times})
    except:
        pass

    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movie_list:
        msg += "⚠️ *BMS temporarily hidden data.*\nClick link below for live shows.\n"
    else:
        for m in movie_list:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])[:50]}...\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book Now](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
