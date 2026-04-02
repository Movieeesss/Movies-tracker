import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import time

# --- Config ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

# Theatre list with correct slugs and IDs
THEATRES = {
    "LA CINEMA (MARIS)": ("la-cinema-maris-trichy", "LATG"),
    "LA CINEMA (SONA MINA)": ("la-cinema-sona-mina-trichy", "SONA"),
    "MEGASTAR CINEMAS": ("megastar-cinemas-trichy", "MMTR"),
    "RAMBA": ("ramba-ac-rgb-laser-dolby-atmos-trichy", "RMBT"),
    "PALACE THEATRE": ("palace-theatre-tiruchirappalli", "PALC"),
    "CAUVERY CINEMAS": ("cauvery-cinemas-4k-rgb-laser-trichy", "CAVY")
}

def get_theatre_data(t_name, t_slug, t_id, date_str):
    # BMS Ticket booking page URL structure
    target_url = f"https://in.bookmyshow.com/buytickets/{t_slug}/cinema-trch-{t_id}-MT/{date_str}"
    
    # Using WebScraping.ai with JS Rendering (since BMS is dynamic)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    movies_found = {}
    try:
        print(f"🔄 Scanning {t_name}...")
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select each movie row/container
            # Note: BMS frequently changes classes, these are the most common ones
            movie_containers = soup.select('li.list, .cinema-showtimes-container')
            
            for container in movie_containers:
                name_tag = container.find('a', class_='__movie-name') or container.select_one('.movie-name')
                
                if name_tag:
                    m_name = name_tag.get_text().strip().upper()
                    
                    # Finding all showtime buttons/pills
                    time_elements = container.select('.showtime-pill, .__showtime, .__session-link, .showtime-pills a')
                    times = []
                    for s in time_elements:
                        t_text = s.get_text().strip()
                        if ":" in t_text:
                            # Clean up text (remove price or 'AM/PM' if needed)
                            clean_time = t_text.split('\n')[0]
                            times.append(clean_time)
                    
                    if m_name and times:
                        # set() used to remove duplicate timings if any
                        movies_found[m_name] = sorted(list(set(times)))
        else:
            print(f"❌ Failed to fetch {t_name}. Status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error scanning {t_name}: {e}")
        
    return movies_found

def run_all():
    # Set IST Time
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    
    full_report = ""
    found_any = False
    
    for name, (slug, v_id) in THEATRES.items():
        results = get_theatre_data(name, slug, v_id, date_str)
        
        if results:
            found_any = True
            full_report += f"📍 *{name}*\n"
            for m, t in results.items():
                full_report += f"🎥 {m}\n🕒 {' | '.join(t)}\n"
            full_report += "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n"
        
        # Adding a small delay to avoid hitting proxy limits too fast
        time.sleep(1)

    # --- Header & Footer ---
    header = f"🏛️ *TRICHY THEATRES LIVE - {ist_now.strftime('%d %b')}* 🏛️\n"
    meta = f"🕒 Updated: {ist_now.strftime('%I:%M %p')}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not found_any:
        full_report = f"⚠️ *Status:* No live data found. Shows might not be open yet or structure changed."
    
    footer = "━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    
    # --- Send to Telegram ---
    payload = {
        "chat_id": CHAT_ID, 
        "text": header + meta + full_report + footer, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": "true"
    }
    
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=payload)
        print("✅ Telegram Report Sent!")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")

if __name__ == "__main__":
    run_all()
