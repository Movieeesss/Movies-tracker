import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
MY_ID = 8095698350  # Unga permanent ID

# Neenga thedura Movie & Date details
MOVIE_NAME = "JANA NAYAGAN"
TARGET_DATE = "20260724" # Date-ah YYYYMMDD format la mathikonga
TARGET_URL = f"https://in.bookmyshow.com/movies/trichy/jana-nayagan/buytickets/ET00430817/{TARGET_DATE}"

def get_movie_showtimes():
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={TARGET_URL}&proxy=stealth&render=true&wait=10000"
    
    theater_data = []
    
    try:
        print(f"Scraping data for {MOVIE_NAME} on {TARGET_DATE}...")
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by BookMyShow Anti-bot (Cloudflare).")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # STRATEGY 1: Extract using BookMyShow's standard 'data-name' attribute
            venues = soup.find_all('li', {'data-name': True})
            if venues:
                for venue in venues:
                    theater_name = venue.get('data-name', '').strip()
                    
                    # Search for time buttons
                    time_tags = venue.find_all('a', {'data-display-showtime': True})
                    timings = [a.get_text().strip() for a in time_tags]
                    
                    if not timings:
                        # Fallback time extraction inside this venue
                        time_elements = venue.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                        timings = [t.strip() for t in time_elements]
                    
                    if theater_name and timings:
                        theater_data.append(f"🏢 *{theater_name}*\n⌚ {', '.join(timings)}")
                        
            # STRATEGY 2: If Strategy 1 fails, search the DOM dynamically for typical venue classes
            if not theater_data:
                for venue_container in soup.find_all(['div', 'li'], class_=re.compile(r'venue|cinema|list', re.I)):
                    name_tag = venue_container.find(['a', 'div', 'strong'], class_=re.compile(r'name|title|venue', re.I))
                    if name_tag:
                        theater_name = name_tag.get_text().strip()
                        
                        # Use regex to find any AM/PM text within this block
                        time_elements = venue_container.find_all(['div', 'a', 'span'], text=re.compile(r'\d{2}:\d{2} [AP]M'))
                        timings = [t.get_text().strip() for t in time_elements]
                        
                        # Avoid garbage text and ensure valid timings exist
                        if theater_name and len(theater_name) > 3 and timings:
                            theater_data.append(f"🏢 *{theater_name}*\n⌚ {', '.join(timings)}")
            
            # Remove any potential duplicate entries
            theater_data = list(dict.fromkeys(theater_data))

        else:
            print(f"⚠️ Scraper Error: HTTP Status Code {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Network/Scraper Error: {e}")
        
    return theater_data

def run_all():
    theaters = get_movie_showtimes()
    
    # Format the Date for Display (e.g., 20260724 -> 24-07-2026)
    display_date = f"{TARGET_DATE[6:8]}-{TARGET_DATE[4:6]}-{TARGET_DATE[0:4]}"
    
    header = f"🎬 *{MOVIE_NAME} - SHOWTIMES* 🎬\n"
    meta = f"📅 *Date:* {display_date}\n📍 *Location:* Trichy\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if theaters is None:
        body = "⚠️ *Status:* Error fetching data (Possible API Block).\n"
    elif len(theaters) == 0:
        body = "⚠️ *Status:* No theaters showing this movie on the selected date. (Structure mismatch or no shows)\n"
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
            data={
                "chat_id": MY_ID, 
                "text": final_msg, 
                "parse_mode": "Markdown", 
                "disable_web_page_preview": "true" 
            }
        )
        print("✅ Message successfully sent to Telegram!")
    except Exception as e: 
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    run_all()
