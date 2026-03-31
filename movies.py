import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_bms_live_data():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = ist_now.strftime("%Y%m%d")
    url = f"https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/{date_str}"
    
    # Chrome Options for GitHub Actions (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    movie_list = []
    driver = None

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(10) # Wait for JavaScript to load movie data
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all('li', class_='list')
        
        for item in listings:
            name_tag = item.find('strong')
            if name_tag:
                name = name_tag.text.strip()
                times = [t.text.strip().split('\n')[0] for t in item.find_all('div', class_='__details') if ":" in t.text]
                if name and times:
                    movie_list.append({"name": name, "times": times})
        
        return movie_list
    except Exception as e:
        print(f"Selenium Error: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def send_to_telegram():
    movies = get_bms_live_data()
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    now_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    if not movies:
        # No message sent if no movies found (to avoid spamming error)
        return

    msg = f"🎬 *LA CINEMAS (MARIS) - LIVE SHOWS* 🎬\n"
    msg += f"🕒 Updated: {now_str}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    
    for m in movies:
        msg += f"🎥 *{m['name']}*\n"
        msg += f"🕒 {', '.join(m['times'])}\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎟️ [Live Booking Link]({url})"

    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    send_to_telegram()
