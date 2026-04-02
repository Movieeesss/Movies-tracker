from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime, timedelta, timezone

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_movies_safe():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # --- MEMORY SAVING OPTIONS ---
    chrome_options.add_argument("--disable-gpu") # GPU disable panna RAM micham aagum
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") # Images load aagadhu
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    
    driver = None
    movie_list = set()
    
    try:
        # Chrome Service setup
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Memory crash thavirkka page load timeout set panrom
        driver.set_page_load_timeout(30)
        driver.get("https://in.bookmyshow.com/explore/movies-trichy")
        
        # Wait for dynamic content
        time.sleep(7) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for h3 in soup.find_all('h3'):
            name = h3.get_text().strip().upper()
            if 3 < len(name) < 45 and not any(x in name for x in ["BOOKING", "OFFER"]):
                movie_list.add(name)
                
    except Exception as e:
        print(f"Memory/Driver Error: {e}")
    finally:
        if driver:
            driver.quit() # Romba mukkiyam: Browser-ah nichayam close pannanum
            
    return sorted(list(movie_list))

def run_all():
    movies = get_movies_safe()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    msg = f"🎬 *TRICHY MOVIES (SELENIUM)* 🎬\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    if not movies:
        msg += "⚠️ *Status:* Memory limit reached or Blocked."
    else:
        for m in movies: msg += f"✅ *{m}*\n"
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
