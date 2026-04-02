import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_la_cinemas_timings():
    # LA Cinema Maris Theater-oda specific URL
    target_url = "https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    theater_data = {} # {Movie Name: [Timings]}
    
    try:
        response = requests.get(proxy_url, timeout=45)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Movie list items-ah loop pandrom
            for movie_li in soup.find_all('li', class_='list'):
                # Movie Name edukkurom
                movie_tag = movie_li.find('a', class_='__movie-name')
                if movie_tag:
                    name = movie_tag.get_text().strip().upper()
                    
                    # Timings edukkurom
                    show_times = []
                    time_tags = movie_li.find_all('div', class_='showtime-pill')
                    for time in time_tags:
                        t = time.get_text().strip()
                        if t: show_times.append(t)
                    
                    if name and show_times:
                        theater_data[name] = show_times
        else:
            print(f"Error: Status {response.status_code}")
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return theater_data

def run_all():
    data = get_la_cinemas_timings()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🍿 *LA CINEMA: MARIS, TRICHY* 🍿\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Booking not yet opened or Theater page updated."
    else:
        body = ""
        for movie, timings in data.items():
            body += f"🎥 *{movie}*\n"
            body += f"🕒 {' | '.join(timings)}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n👉 [Book Now](https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT)"
    
    final_msg = header + meta + body + footer
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
