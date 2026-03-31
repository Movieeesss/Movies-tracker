import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_la_maris_shows():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{date_str}"
    
    # Simple Request with better headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_list = []
        
        # BMS listings updated logic
        for item in soup.find_all('li', class_='list'):
            name = item.find('strong').text.strip() if item.find('strong') else ""
            times = [t.text.strip() for t in item.find_all('div', class_='__details')]
            if name and times:
                movie_list.append({"name": name, "times": times})
        return movie_list
    except:
        return []

# Baaki send_to_telegram function adhe thaan...
