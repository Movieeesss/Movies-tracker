import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"
SCRAPER_API_KEY = "9919328312a5982c5b8bca398de8a5ef" # Unga key-ah add pannitten

def run_all():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    target_url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{ist_now.strftime('%Y%m%d')}"
    
    # ScraperAPI Logic - Idhu unga request-ah real Indian user maadhiri mathum
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&render=true&country_code=in"
    
    movie_list = []
    try:
        # Rendering enabled so JavaScript movies load aagum
        response = requests.get(proxy_url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BMS listings target
        listings = soup.find_all('li', class_='list')
        for item in listings:
            name_tag = item.find('strong')
            if name_tag:
                name = name_tag.get_text(strip=True)
                # Show timings check
                times = [t.get_text(strip=True) for t in item.find_all('div', class_='__details') if ":" in t.text]
                if name and times:
                    movie_list.append({"name": name, "times": times})
    except Exception as e:
        print(f"Proxy Error: {e}")

    # Message Formatting
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    msg += f"🕒 Updated: {time_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movie_list:
        msg += "⚠️ *BMS Security Alert.*\nProxy route-layum data kidaikala.\n"
        msg += "Try checking the link below manually.\n"
    else:
        for m in movie_list:
            msg += f"🎥 *{m['name']}*\n"
            msg += f"🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🎟️ [Direct Booking Link]({target_url})"

    # Send to Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    })

if __name__ == "__main__":
    run_all()
