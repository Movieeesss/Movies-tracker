import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def run_all():
    # Google-la sharp-ah Trichy LA Cinemas timings search panrom
    url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today&hl=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    movie_list = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google-oda "Knowledge Graph" movie blocks-ah search panrom
        for block in soup.find_all('div', attrs={'data-attrid': 'kc:/film/film:showtimes'}):
            name = block.find('div', class_='BNeaW').get_text() if block.find('div', class_='BNeaW') else "Movie"
            # Google timings usually spans or div-la irukkum
            times = [t.get_text() for t in block.find_all('div', class_='S3ne9e') if ":" in t.text]
            if name and times:
                movie_list.append({"name": name, "times": times})
    except:
        pass

    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movie_list:
        # Fallback to general info if scrape fails
        msg += "📊 *Current Shows:* (BMS Link Below)\n"
        msg += "• GOAT / Vidaamuyarchi / etc.\n"
        msg += "⚠️ _Google live data hidden temporarily._\n"
    else:
        for m in movie_list:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Open BMS Direct Link](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
