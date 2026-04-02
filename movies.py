import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_la_cinemas_timings():
    # Naalaikku date calculate panrom (YYYYMMDD format)
    ist_tomorrow = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30, days=1)
    date_str = ist_tomorrow.strftime("%Y%m%d")
    
    # URL-la date-ah dynamic-ah add panrom
    target_url = f"https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT/{date_str}"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    theater_data = {}
    try:
        response = requests.get(proxy_url, timeout=45)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Movie list extraction
            for movie_li in soup.find_all('li', class_='list'):
                movie_tag = movie_li.find('a', class_='__movie-name')
                if movie_tag:
                    name = movie_tag.get_text().strip().upper()
                    
                    show_times = []
                    # BMS-la timings 'showtime-pill' or '.__showtime' kulla irukkum
                    time_tags = movie_li.select('.showtime-pill, .__showtime')
                    for time in time_tags:
                        t = time.get_text().strip()
                        if t and ":" in t: # Proper time format check
                            show_times.append(t)
                    
                    if name and show_times:
                        theater_data[name] = show_times
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        
    return theater_data, date_str

def run_all():
    data, check_date = get_la_cinemas_timings()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    # Header-la check panra date-ah kaatuvom
    formatted_date = datetime.strptime(check_date, "%Y%m%d").strftime("%d-%b")
    header = f"🍿 *LA CINEMA - {formatted_date} SHOWS* 🍿\n"
    meta = f"🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Tomorrow's booking not yet found in our scan.\n"
    else:
        body = ""
        for movie, timings in data.items():
            body += f"🎥 *{movie}*\n"
            # Unwanted texts filter panni timings mattum clean-ah kaatuvom
            clean_times = [t.split('\n')[0] for t in timings]
            body += f"🕒 {' | '.join(clean_times)}\n\n"
            
    footer = f"━━━━━━━━━━━━━━━━━━━━\n👉 [Check Tomorrow's Shows](https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-LACN-MT/{check_date})"
    
    final_msg = header + meta + body + footer
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": "true"})

if __name__ == "__main__":
    run_all()
