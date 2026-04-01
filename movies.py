import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def run_all():
    # Direct Google Search via Mobile User-Agent (Blocks thavirkka)
    url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Google mobile result-la timings "Showtimes" nu search pannum
        text = soup.get_text()
        import re
        times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)', text)
        
        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
        
        msg = f"🎬 *LA CINEMAS - MOBILE SCRAPER* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
        
        if not times:
            msg += "⚠️ No timings found. Google is blocking the request.\n"
        else:
            msg += f"🎥 *Today's Shows:*\n🕒 {', '.join(list(dict.fromkeys(times)))}\n"
            
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

if __name__ == "__main__":
    run_all()
