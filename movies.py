import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Bot Settings
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
API_KEY = "1c52b530-7d6e-4a64-b061-85cc76e6e937"

def get_booking_open_movies():
    # Trichy city-oda movies listing page
    target_url = "https://in.bookmyshow.com/explore/movies-tiruchirappalli"
    
    # Webscraping.ai use panni page render panrom (JS load aaga 15s wait)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    available_movies = []
    try:
        print("Scanning BookMyShow for live bookings...")
        response = requests.get(proxy_url, timeout=180)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BMS-la ovvoru movie card-um oru specific div-kulla irukkum
            # 'commonStyles__Card' kulla title matrum booking status irukkum
            movie_cards = soup.find_all('div', style=re.compile(r'cursor: pointer', re.I))
            
            for card in movie_cards:
                # Movie Name extraction
                name_tag = card.find('div', class_=re.compile(r'CardTitle', re.I))
                if not name_tag:
                    continue
                
                name = name_tag.get_text(strip=True).upper()
                
                # Booking Open-ah nu check panna 'Book' nu text irukka nu paarkuroom
                # Sila neram 'Coming Soon' nu irukkum, athai skip pannuvom
                card_text = card.get_text(" ", strip=True).lower()
                
                # 'book' appadira vaarthai irunthaal mattum list-la add pannuvom
                if 'book' in card_text and 'coming soon' not in card_text:
                    available_movies.append(name)
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Scraping Error: {e}")
        
    # Duplicate-ah remove panni sort pannuvom
    return sorted(list(set(available_movies)))

def run_all():
    # Trigger Start Notification
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🔍 *Scanning for Movies with Open Bookings...*", "parse_mode": "Markdown"})
    
    movies = get_booking_open_movies()
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎟️ *TRICHY - BOOKING OPEN NOW* 🎟️\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* Booking not yet open for current listings.\n"
        body += "💡 _Check back in 15 mins._\n"
    else:
        body = "🎥 *BOOKING OPEN FOR:*\n\n"
        for m in movies:
            body += f"✅ *{m}*\n"
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n👉 [Book on BMS](https://in.bookmyshow.com/explore/movies-tiruchirappalli)"
    
    # Final message send
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
