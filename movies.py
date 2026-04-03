import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
API_KEY = "MKDCNDT9VWVFGX57CQ5NCR9R40F4FZWHDSLF98Z1KEK0NN5F9ZNKOM6GT5UDKD9YB6IO3A7WLNAAEHY0"
MY_ID = 1115358053  

def get_movies_from_google():
    # Google search query for Maris timings
    search_url = "https://www.google.com/search?q=LA+Cinema+Maris+Trichy+movie+timings+tomorrow"
    
    params = {
        'api_key': API_KEY,
        'url': search_url,
        'render_js': 'true',
        'premium_proxy': 'true',
        'country_code': 'in',
        'wait': '5000'
    }
    
    movie_results = []
    try:
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Google search result-la movie cards target panrom
            # Usually 'rllt__details' or 'div' with specific text
            results = soup.find_all('div', class_='Vkp9Pc') or soup.find_all('div', class_='rllt__details')
            
            for res in results:
                text = res.get_text(separator=" ", strip=True)
                # Filtering for timings and names
                if "AM" in text or "PM" in text:
                    movie_results.append(f"🎬 {text}")
                    
        return list(dict.fromkeys(movie_results))[:10]
    except:
        return []

def run_all():
    data = get_movies_from_google()
    
    header = "🎥 *LA CINEMA (MARIS) - GOOGLE LIVE DATA* 🎥\n━━━━━━━━━━━━━━━━━━━━\n"
    body = "\n\n".join(data) if data else "⚠️ *Status:* Google data blocked. Site security high."
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n🎫 Book on: lacucinema.com"
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": MY_ID, "text": header + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
