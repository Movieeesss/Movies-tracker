import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_timings():
    # Google Search URL for precise local result
    target_url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today&hl=en"
    
    # Using ScraperAPI to bypass Google's bot detection
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in&render=true"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google "Showtimes" card logic
        # Typically found in divs with specific data attributes
        for movie_block in soup.find_all('div', attrs={'data-attrid': 'kc:/film/film:showtimes'}):
            try:
                name = movie_block.find('div', class_='BNeaW').get_text()
                # Finding all timings (e.g., 10:30 AM, 2:15 PM)
                time_elements = movie_block.find_all('div', class_='S3ne9e')
                times = [t.get_text() for t in time_elements if ":" in t.text]
                
                if name and times:
                    movie_results.append({"name": name, "times": times})
            except:
                continue
                
    except Exception as e:
        print(f"Scrape Error: {e}")
    
    return movie_results

def run_all():
    movies = get_movie_timings()
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater data is syncing...\n"
        msg += "⚠️ _Google currently updating live timings._\n"
        msg += "💡 _Click link below for instant check._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Check & Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    run_all()
