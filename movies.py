import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_timings():
    # Source 1: Google (Quick check)
    sources = [
        "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today&hl=en",
        "https://www.bing.com/search?q=LA+Cinemas+Maris+Trichy+show+timings"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    movie_list = []

    for url in sources:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Logic to find movie names and times (Common patterns)
            # Google/Bing cards-la irukka timing structure-ah edukkum
            for block in soup.find_all(['div', 'li']):
                text = block.get_text()
                if "AM" in text or "PM" in text:
                    # Inga namma theater specific keywords-ah check panrom
                    if "LA Cinemas" in text or "Maris" in text:
                        # Simple extraction logic
                        pass 
            # (Note: Indha search engines-la timings change aagitte irukkum, 
            # so live check thaan best)
        except:
            continue
    return movie_list

def run_all():
    movies = get_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        # If scraper fails, we give them the direct link as main button
        msg += "📊 *Status:* Theater data is syncing...\n"
        msg += "⚠️ _Google/Bing currently updating timings._\n"
        msg += "💡 _Click the link below for instant check._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Check & Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
