import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
MY_ID = 8095698350  

MOVIE_NAME = "JANA NAYAGAN"
TARGET_DATE = "20260724" 
TARGET_URL = f"https://in.bookmyshow.com/movies/trichy/jana-nayagan/buytickets/ET00430817/{TARGET_DATE}"

def get_movie_showtimes():
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={TARGET_URL}&proxy=stealth&render=true&wait=10000"
    
    theater_data = []
    
    try:
        print(f"Scraping data for {MOVIE_NAME} on {TARGET_DATE}...")
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by Anti-bot.")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # FIX: Isolate exact theater rows and ignore hidden sidebar menus
            venue_links = soup.find_all('a', href=re.compile(r'/cinemas/|/venue/', re.I))
            
            for a in venue_links:
                theater_name = a.get_text().strip()
                if len(theater_name) < 3: 
                    continue
                
                # Navigate up to find the exact row container for THIS specific theater
                parent = a.parent
                valid_container = None
                
                for _ in range(4): # Typically the row wrapper is 3-4 levels up
                    if parent:
                        times_in_parent = parent.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                        if times_in_parent:
                            valid_container = parent
                            break
                        parent = parent.parent
                        
                if valid_container:
                    # Extract times STRICTLY inside this specific row
                    times = valid_container.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                    times = [t.strip() for t in times if t.strip()]
                    times = list(dict.fromkeys(times))
                    
                    # Fix for copy-paste bug: Ignore huge containers that accidentally grab the whole page
                    if times and len(times) <= 12: 
                        entry = f"🏢 *{theater_name}*\n⌚ {', '.join(times)}"
                        if entry not in theater_data:
                            theater_data.append(entry)

        else:
            print(f"⚠️ Scraper Error: HTTP Status Code {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Network/Scraper Error: {e}")
        
    return theater_data

def run_all():
    theaters = get_movie_showtimes()
    
    display_date = f"{TARGET_DATE[6:8]}-{TARGET_DATE[4:6]}-{TARGET_DATE[0:4]}"
    
    header = f"🎬 *{MOVIE_NAME} - SHOWTIMES* 🎬\n"
    meta = f"📅 *Date:* {display_date}\n📍 *Location:* Trichy\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if theaters is None:
        body = "⚠️ *Status:* Error fetching data.\n"
    elif len(theaters) == 0:
        body = "⚠️ *Status:* No theaters showing this movie yet.\n"
    else:
        body = ""
        for t in theaters:
            body += f"{t}\n\n"
            
    footer = f"━━━━━━━━━━━━━━━━━━━━\n🔗 [Book Tickets Now]({TARGET_URL})"
    final_msg = header + meta + body + footer

    try:
        print("Sending message to Telegram...")
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
            data={"chat_id": MY_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"}
        )
        print("✅ Success!")
    except Exception as e: 
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    run_all()
