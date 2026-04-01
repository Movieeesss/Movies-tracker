import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_timings():
    # Target: Google Search Results (BMS timings are usually in snippets)
    query = "LA+Cinemas+Maris+Trichy+show+timings+today"
    target_url = f"https://www.google.com/search?q={query}&hl=en"
    
    # Simple Proxy without heavy rendering to avoid bot detection
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google search results text-ah full-aa edukkirom
        all_text = soup.get_text()
        
        # Common movie names in Trichy right now (Example list - update as needed)
        # Or better: Look for patterns like "Movie Name ... 10:30 AM, 2:15 PM"
        # Since searching in 'div' cards is safer:
        for card in soup.find_all('div', class_='g'): # Standard Google result class
            text = card.get_text()
            if "LA Cinema" in text or "Maris" in text:
                # Timings find panna regex or logic
                import re
                times = re.findall(r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)', text)
                if times:
                    movie_results.append({"name": "Current Movies", "times": list(dict.fromkeys(times))})
                    break

    except Exception as e:
        print(f"Stealth Error: {e}")
    
    return movie_results

def run_all():
    movies = get_movie_timings()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater data is syncing...\n"
        msg += "⚠️ _BMS security is very tight today._\n"
        msg += "💡 _Checking Google Search cache._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
