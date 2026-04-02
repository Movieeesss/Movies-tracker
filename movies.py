import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import time

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

# Theatre Names and their EXACT URL slugs from BMS
THEATRES = {
    "LA CINEMA (MARIS)": ("la-cinema-maris-trichy", "LATG"),
    "LA CINEMA (SONA MINA)": ("la-cinema-sona-mina-trichy", "SONA"),
    "MEGASTAR CINEMAS": ("megastar-cinemas-trichy", "MMTR"),
    "RAMBA": ("ramba-ac-rgb-laser-dolby-atmos-trichy", "RMBT"),
    "PALACE THEATRE": ("palace-theatre-tiruchirappalli", "PALC"),
    "CAUVERY CINEMAS": ("cauvery-cinemas-4k-rgb-laser-trichy", "CAVY")
}

def get_theatre_data(t_name, t_slug, t_id, date_str):
    # Correct URL structure for each theater
    target_url = f"https://in.bookmyshow.com/buytickets/{t_slug}/cinema-trch-{t_id}-MT/{date_str}"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    movies_found = {}
    try:
        response = requests.get(proxy_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Checking movie containers
            for movie_li in soup.select('li.list'):
                name_tag = movie_li.find('a', class_='__movie-name')
                if name_tag:
                    m_name = name_tag.get_text().strip().upper()
                    # Timing extraction (session-link covers more theaters)
                    times = [s.get_text().strip().split('\n')[0] for s in movie_li.select('.showtime-pill, .__showtime, .__session-link') if ":" in s.get_text()]
                    if m_name and times:
                        movies_found[m_name] = sorted(list(set(times)))
    except Exception as e:
        print(f"Error scanning {t_name}: {e}")
    return movies_found

def run_all():
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    # Midnight Fix: If it's very early (before 1 AM), check for the same day shows.
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
        time.sleep(2) # API protection delay

    header = f"🏛️ *TRICHY THEATRES LIVE - {ist_now.strftime('%d %b')}* 🏛️\n"
    meta = f"🕒 Updated: {ist_now.strftime('%I:%M %p')}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not found_any:
        full_report = f"⚠️ *Status:* No live data found. Shows for {ist_now.strftime('%d-%b')} might not be updated yet or page structure changed."
    
    footer = "━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": header + meta + full_report + footer, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
