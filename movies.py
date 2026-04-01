import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_google_movie_data():
    # Google Search URL for LA Cinemas Maris Trichy
    url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+movie+timings&hl=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    movie_list = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google Movie Card extraction logic
        # Note: Google changes classes often, so we look for 'data-attrid'
        containers = soup.find_all('div', attrs={'data-attrid': 'kc:/film/film:showtimes'})
        
        for container in containers:
            name = container.find('div', class_='BNeaW').get_text() if container.find('div', class_='BNeaW') else "Movie"
            # Timings extract
            times = [t.get_text() for t in container.find_all('div', class_='S3ne9e') if ":" in t.text]
            if name and times:
                movie_list.append({"name": name, "times": times})
                
        return movie_list
    except:
        return []

def send_telegram():
    movies = get_google_movie_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - GOOGLE LIVE* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "⚠️ Live data fetch tough on US Server.\n"
        msg += "🎟️ [Check BMS Direct](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n"
            msg += f"🕒 {', '.join(m['times'])}\n\n"
            
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    send_telegram()
