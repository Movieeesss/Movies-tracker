import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef"

def get_movie_data():
    # Targeted Search for LA Cinemas Maris Trichy
    target_url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings+today&hl=en"
    # Using Premium ScraperAPI settings with India Proxy
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&country_code=in&render=true&wait_until=networkidle"
    
    movie_results = []
    try:
        response = requests.get(proxy_url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # METHOD 1: Target Google's Official Showtimes Card
        # Inga namma multiple possible classes-ah check panrom
        blocks = soup.find_all('div', attrs={'data-attrid': re.compile(r'kc:/film/film:showtimes|kc:/film/film:theatre_showtimes')})
        
        # Method 2: If Method 1 fails, find by common text patterns (Showtimes container)
        if not blocks:
            blocks = soup.find_all('div', class_=re.compile(r'showtimes|theatre'))

        for block in blocks:
            try:
                # Movie Name Extraction (Heading tags)
                name_tag = block.find(['div', 'span'], attrs={'data-attrid': 'title'}) or block.find('div', class_='BNeaW')
                name = name_tag.get_text() if name_tag else "Currently Playing"
                
                # Timings Extraction (Look for AM/PM patterns)
                times = []
                # All spans/divs that look like time
                potential_times = block.find_all(['div', 'span', 'a'])
                for pt in potential_times:
                    t_text = pt.get_text(strip=True)
                    # Regex logic: 10:30 AM, 2:45 PM patterns
                    if ":" in t_text and ("AM" in t_text or "PM" in t_text):
                        times.append(t_text)
                
                # Deduplicate times and clean up
                times = list(dict.fromkeys(times))
                
                if times:
                    movie_results.append({"name": name, "times": times})
            except:
                continue
                
    except Exception as e:
        print(f"Deep Scrape Error: {e}")
    
    return movie_results

import re # Required for regex search

def run_all():
    movies = get_movie_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        msg += "📊 *Status:* Theater syncing live timings...\n"
        msg += "⚠️ _Google is refreshing today's schedule._\n"
        msg += "💡 _Try hitting the update link again._\n"
    else:
        for m in movies:
            msg += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/)"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    run_all()
