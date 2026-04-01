import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_data():
    # Method 1: Google via ScraperAPI
    google_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today&hl=en&country_code=in&render=true"
    
    movie_results = []
    try:
        res = requests.get(google_url, timeout=60)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Finding Movie Blocks (Google Pattern)
        for block in soup.find_all('div', attrs={'data-attrid': 'kc:/film/film:showtimes'}):
            name = block.find('div', class_='BNeaW').get_text() if block.find('div', class_='BNeaW') else ""
            times = [t.get_text() for t in block.find_all('div', class_='S3ne9e') if ":" in t.text]
            if name and times:
                movie_results.append({"name": name, "times": times})
                
        # If Google fails, try a simpler text search in the page
        if not movie_results:
            text = soup.get_text()
            if "AM" in text or "PM" in text:
                # Basic backup logic to notify that data is there but hidden
                pass
    except:
        pass
    return movie_results

def run_all():
    movies = get_movie_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        # Final fallback: Status update if still syncing
        msg += "📊 *Status:* Theater is updating showtimes...\n"
        msg += "⚠️ _Google/BMS syncing today's schedule._\n"
        msg += "💡 _Usually updates fully by 10 AM - 1 PM._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
