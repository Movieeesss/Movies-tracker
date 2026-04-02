import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_all_trichy_theatres():
    # Trichy overall movies page - Idhula dhaan ella theatre-um list aagum
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    
    target_url = f"https://in.bookmyshow.com/explore/movies-trichy"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=25000"
    
    all_data = {} # {Movie: {Theatre: [Timings]}}
    
    try:
        response = requests.get(proxy_url, timeout=120)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Movies list-ah find panrom
            for movie_card in soup.select('.commonStyles__MovieCardWrapper'):
                m_name = movie_card.find('h3').get_text().strip().upper()
                all_data[m_name] = []
                
        # Better Logic: Instead of main page, theatre-wise scan is more stable
        # Popular Trichy Venue IDs:
        theatres = {
            "LA CINEMA": "LATG",
            "RAMBA": "RMBT",
            "SONA MEENA": "SONA",
            "MEGA MAHARANI": "MMTR",
            "PALACE THEATRE": "PALC"
        }
        
        final_report = {}
        
        for t_name, t_id in theatres.items():
            t_url = f"https://in.bookmyshow.com/buytickets/la-cinema-maris-trichy/cinema-trch-{t_id}-MT/{date_str}"
            t_proxy = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={t_url}&proxy=residential&render=true&wait=15000"
            
            t_res = requests.get(t_proxy, timeout=60)
            if t_res.status_code == 200:
                t_soup = BeautifulSoup(t_res.text, 'html.parser')
                current_theatre_movies = {}
                
                for m_li in t_soup.select('li.list'):
                    name = m_li.find('a', class_='__movie-name').get_text().strip().upper()
                    shows = [s.get_text().strip().split('\n')[0] for s in m_li.select('.showtime-pill, .__showtime') if ":" in s.get_text()]
                    if name and shows:
                        current_theatre_movies[name] = shows
                
                if current_theatre_movies:
                    final_report[t_name] = current_theatre_movies
                    
    except Exception as e:
        print(f"Error: {e}")
        
    return final_report, date_str

def run_all():
    data, d_str = get_all_trichy_theatres()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = f"🏛️ *TRICHY ALL THEATRES LIVE* 🏛️\n"
    meta = f"🕒 Updated: {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No live theatre data found. Try again later."
    else:
        body = ""
        for t_name, movies in data.items():
            body += f"📍 *{t_name}*\n"
            for m_name, times in movies.items():
                body += f"🎥 {m_name}\n🕒 {' | '.join(times)}\n"
            body += "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n👉 [Open BMS](https://in.bookmyshow.com/explore/movies-trichy)"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
