import requests
import re
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
MY_ID = 8095698350  # Unga permanent ID

MOVIE_NAME = "JANA NAYAGAN"
TARGET_DATE = "20260724" # Date-ah YYYYMMDD format la vachikonga
TARGET_URL = f"https://in.bookmyshow.com/movies/trichy/jana-nayagan/buytickets/ET00430817/{TARGET_DATE}"

def get_movie_showtimes():
    # Added js=true and wait=15000 to force the proxy to wait for the JavaScript to fully render the theaters
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={TARGET_URL}&proxy=stealth&js=true&render=true&wait=15000"
    
    theater_data = []
    seen_theaters = set()
    
    try:
        print(f"Scraping data for {MOVIE_NAME} on {TARGET_DATE} (Waiting for JS to load)...")
        response = requests.get(proxy_url, timeout=90) # Increased timeout to handle the 15s wait
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by Anti-bot (Cloudflare).")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Master Strategy: Find ALL theater links directly
            venue_links = soup.find_all('a', href=re.compile(r'/cinemas/|/venue/', re.I))
            
            for a in venue_links:
                theater_name = a.get_text().strip()
                if len(theater_name) < 3 or theater_name in seen_theaters: 
                    continue
                
                # Navigate up the HTML tree to find the specific row for this theater
                current = a.parent
                valid_container = None
                
                # Walk up to 6 levels to find the container holding both the name and the times
                for _ in range(6):
                    if current and current.name != 'body':
                        times_found = current.find_all(text=re.compile(r'\d{2}:\d{2} [AP]M'))
                        if times_found:
                            # Verify we haven't jumped to the whole page container
                            nested_theaters = current.find_all('a', href=re.compile(r'/cinemas/|/venue/', re.I))
                            if len(nested_theaters) <= 2: # Keep it specific to this row
                                valid_container = current
                                break
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
        body = "⚠️ *Status:* Error fetching data (Possible API Block).\n"
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
