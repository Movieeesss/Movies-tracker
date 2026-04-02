import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_la_cinemas_timings():
    # Naalaikku (April 03) date calculate panrom
    ist_tomorrow = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30, days=1)
    date_str = ist_tomorrow.strftime("%Y%m%d") # Format: 20260403
    
    target_url = f"https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT/{date_str}"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    theater_data = {}
    try:
        response = requests.get(proxy_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS-la ovvoru movie-um 'list' class ulla irukkum
            movie_containers = soup.find_all('li', class_='list')
            
            for container in movie_containers:
                # Movie Name extraction
                name_tag = container.find('a', class_='__movie-name')
                if not name_tag: continue
                movie_name = name_tag.get_text().strip().upper()
                
                # Show timings extraction
                # Multiple possible classes-ah check panrom
                time_tags = container.find_all(['div', 'a'], class_=lambda x: x and ('showtime-pill' in x or 'time' in x.lower()))
                
                timings = []
                for t_tag in time_tags:
                    time_text = t_tag.get_text().strip()
                    # Filtering: 11:00 AM maari format-la irukra text-ah mattum edukka
                    if any(char.isdigit() for char in time_text) and (":" in time_text):
                        # Text-la irukra extra details (Dolby, 4K) remove panna split panrom
                        clean_time = time_text.split('\n')[0].strip()
                        if clean_time not in timings:
                            timings.append(clean_time)
                
                if movie_name and timings:
                    theater_data[movie_name] = sorted(list(set(timings)))
        else:
            print(f"Scraper Error: {response.status_code}")
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return theater_data, date_str

def run_all():
    data, check_date = get_la_cinemas_timings()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    formatted_date = datetime.strptime(check_date, "%Y%m%d").strftime("%d-%b")
    
    header = f"🍿 *LA CINEMA - {formatted_date} SHOWS* 🍿\n"
    meta = f"🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = f"⚠️ *Status:* Booking data not found for {formatted_date} yet.\n"
    else:
        body = ""
        for movie, timings in data.items():
            body += f"🎥 *{movie}*\n"
            body += f"🕒 {' | '.join(timings)}\n\n"
            
    footer = f"━━━━━━━━━━━━━━━━━━━━\n👉 [Book Now](https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT/{check_date})"
    
    final_msg = header + meta + body + footer
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
