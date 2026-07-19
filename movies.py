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

def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
            data={"chat_id": MY_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"}
        )
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_movie_showtimes():
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={TARGET_URL}&proxy=stealth&js=true&wait=15000"
    
    theater_data = []
    
    try:
        print(f"Scraping data for {MOVIE_NAME}...")
        response = requests.get(proxy_url, timeout=90)
        
        if response.status_code == 200:
            html = response.text
            
            # Check for bot blocks
            if "Just a moment..." in html or "Cloudflare" in html:
                return "BLOCKED"
            
            soup = BeautifulSoup(html, 'html.parser')
            seen_theaters = set()

            # STRATEGY 1: Desktop View (data-name tag)
            for li in soup.find_all(attrs={'data-name': True}):
                name = li.get('data-name').strip()
                times = [t.text.strip() for t in li.find_all(attrs={'data-display-showtime': True})]
                if not times:
                    times = [t.strip() for t in re.findall(r'\d{1,2}:\d{2}\s*[APap][Mm]', li.text)]
                
                if name and times and name not in seen_theaters:
                    times = list(dict.fromkeys(times))
                    theater_data.append(f"🏢 *{name}*\n⌚ {', '.join(times)}")
                    seen_theaters.add(name)

            # STRATEGY 2: Mobile View (venue-name classes)
            if not theater_data:
                venues = soup.find_all(['a', 'div'], class_=re.compile(r'venue.*?name', re.I))
                for v in venues:
                    name = v.text.strip()
                    parent = v.find_parent(['li', 'div', 'ul', 'section'])
                    if parent:
                        times = [t.strip() for t in re.findall(r'\d{1,2}:\d{2}\s*[APap][Mm]', parent.text)]
                        if name and len(name) > 3 and times and name not in seen_theaters:
                            times = list(dict.fromkeys(times))
                            theater_data.append(f"🏢 *{name}*\n⌚ {', '.join(times)}")
                            seen_theaters.add(name)

            # STRATEGY 3: Debug Mode - If nothing is found, return the page title and start of body
            if not theater_data:
                page_title = soup.title.string if soup.title else "No Title"
                clean_body = re.sub(r'\s+', ' ', soup.text) # Clean up huge spaces
                snippet = clean_body[:300] if len(clean_body) > 10 else html[:300]
                return f"NO_DATA|Title: {page_title} | Content: {snippet}"

        else:
            return f"ERROR_{response.status_code}"
            
    except Exception as e:
        return f"EXCEPTION: {e}"
        
    return theater_data

def run_all():
    theaters = get_movie_showtimes()
    
    display_date = f"{TARGET_DATE[6:8]}-{TARGET_DATE[4:6]}-{TARGET_DATE[0:4]}"
    header = f"🎬 *{MOVIE_NAME} - SHOWTIMES* 🎬\n📅 *Date:* {display_date}\n📍 *Location:* Trichy\n━━━━━━━━━━━━━━━━━━━━\n\n"
    footer = f"\n━━━━━━━━━━━━━━━━━━━━\n🔗 [Book Tickets Now]({TARGET_URL})"

    if theaters == "BLOCKED":
        msg = header + "⚠️ *Status:* Blocked by BookMyShow Security." + footer
    elif isinstance(theaters, str) and theaters.startswith("NO_DATA|"):
        debug_info = theaters.replace("NO_DATA|", "").strip()
        msg = header + f"⚠️ *Status:* Theaters not found. API sent this instead:\n\n`{debug_info}`" + footer
    elif isinstance(theaters, str) and theaters.startswith("ERROR"):
        msg = header + f"⚠️ *Status:* Scraper API Error ({theaters})." + footer
    elif isinstance(theaters, str) and theaters.startswith("EXCEPTION"):
        msg = header + f"⚠️ *Status:* Network timeout or error." + footer
    elif not theaters:
        msg = header + "⚠️ *Status:* No theaters showing this movie yet." + footer
    else:
        body = "\n\n".join(theaters)
        msg = header + body + footer

    print("Sending message to Telegram...")
    send_telegram(msg)
    print("✅ Done!")

if __name__ == "__main__":
    run_all()
