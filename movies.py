import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_la_maris_v2():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    # Live URL
    url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{date_str}"
    
    # Real Chrome Mobile User Agent (Android)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://in.bookmyshow.com/trichy/cinemas',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1'
    }
    
    movie_list = []
    try:
        # Session use panna BMS detect panna kashtam
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('li', class_='list'):
                name = item.find('strong').text.strip() if item.find('strong') else ""
                times = [t.text.strip().split('\n')[0] for t in item.find_all('div', class_='__details') if ":" in t.text]
                if name and times:
                    movie_list.append({"name": name, "times": times})
        return movie_list
    except:
        return []

def send_update():
    movies = get_la_maris_v2()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    now_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    # Message Logic
    if not movies:
        # If still blocked, send a "Manual Link" message so you don't miss out
        msg = f"🎬 *LA CINEMAS (MARIS) - TRICHY* 🎬\n"
        msg += f"🕒 Updated: {now_str}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        msg += "⚠️ *BMS Security Alert:* Bot blocked by server.\n"
        msg += "Live fetch is tough from US servers.\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        msg += "🎟️ [Click here for Live Timings](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    else:
        msg = f"🎬 *LA CINEMAS (MARIS) - LIVE SHOWS* 🎬\n"
        msg += f"🕒 Updated: {now_str}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        for m in movies:
            msg += f"🎥 *{m['name']}*\n"
            msg += f"🕒 {', '.join(m['times'])}\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        msg += "🎟️ [Book Now](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    send_update()
