import requests
import re
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A")
CHAT_ID = os.getenv("1115358053")
API_KEY = os.getenv("1c52b530-7d6e-4a64-b061-85cc76e6e937")

def get_movie_timings():
    url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/"
    
    proxy = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={url}&render=true"
    
    try:
        res = requests.get(proxy, timeout=60)
        text = res.text

        times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM)', text)
        times = list(dict.fromkeys(times))

        return times

    except Exception as e:
        print("ERROR:", e)
        return []


def run_all():
    times = get_movie_timings()
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 LA CINEMAS MARIS\n🕒 {time_str}\n\n"

    if not times:
        msg += "⚠️ No timings found"
    else:
        msg += "🎥 Showtimes:\n"
        msg += ", ".join(times)

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}
    )
