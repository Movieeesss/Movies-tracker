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
    seen_theaters = set()
    
    try:
        print(f"Scraping data for {MOVIE_NAME} on {TARGET_DATE}...")
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by Anti-bot.")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all theater links
            venue_links = soup.find_all('a', href=re.compile(r'/cinemas/|/venue/', re.I))
            
            for a in venue_links:
                theater_name = a.get_text().strip()
                if len(theater_name) < 3 or theater_name in seen_theaters: 
                    continue
                
                current = a.parent
                valid_container = None
                
                # Smart DOM Walker: Walk up the HTML tree to find the exact row
                while current and current.name != 'body':
                    # Search for times in current container
                    times_found = current.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                    
                    if times_found:
                        # Safety check: Ensure we haven't gone too high and grabbed the whole page
                        nested_theaters = current.find_all('a', href=re.compile(r'/cinemas/|/venue/', re.I))
                        unique_theaters = set([nt.get_text().strip() for nt in nested_theaters if len(nt.get_text().strip()) > 2])
                        
                        if len(unique_theaters) <= 1:
                            valid_container = current
                            break # We found the perfect row!
                        else:
                            break # Went too high, stop looking
                            
                    current = current.parent
                        
                if valid_container:
                    raw_times = valid_container.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                    times = [t.strip() for t in raw_times if t.strip()]
                    times = list(dict.fromkeys(times)) # Remove duplicates
                    
                    if times:
                        theater_data.append(f"🏢 *{theater_name}*\n⌚ {', '.join(times)}")
                        seen_theaters.add(theater_name)

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
