import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def run_all():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    
    # BMS Direct URL
    url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{date_str}"
    
    # Indha headers thaan romba mukkiyam - Idhu real mobile user maadhiri nadakkum
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://in.bookmyshow.com/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    movie_list = []
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BMS-la movie blocks-ah ippo find panrom
        listings = soup.find_all('li', class_='list')
        
        if not listings:
            # Plan B: Try a different tag structure if first one fails
            listings = soup.select('.cinema-showtimes')

        for item in listings:
            # Movie Name extraction
            name_tag = item.find('strong') or item.find('a', class_='__movie-name')
            if name_tag:
                name = name_tag.get_text(strip=True)
                
                # Show timings extraction
                times_list = []
                # Finding timings in the button/link structure
                time_tags = item.find_all('a', attrs={'data-showtime-code': True}) or item.find_all('div', class_='__details')
                
                for t in time_tags:
                    t_text = t.get_text(strip=True).split('\n')[0]
                    if ":" in t_text: # Sharp-ah time format-ah mattum edukkum
                        times_list.append(t_text)
                
                if name and times_list:
                    movie_list.append({"name": name, "times": list(dict.fromkeys(times_list))}) # Remove duplicates

    except Exception as e:
        print(f"Error: {e}")

    # Message Formatting
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movie_list:
        msg += "⚠️ *BMS Data Locked.*\nServer is currently protecting showtimes.\n"
        msg += "Try checking via the link below.\n"
    else:
        for m in movie_list:
            msg += f"🎥 *{m['name']}*\n"
            msg += f"🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🎟️ [Direct Booking Link]({url})"

    # Send to Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    })

if __name__ == "__main__":
    run_all()
