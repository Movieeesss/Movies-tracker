import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TOKEN = "8825463319:AAH285s09kaeYMTXsPCEd41gjiTA-GQbL7g"
API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
USER_FILE = "users.json"
MY_ID = 8095698350  # Unga permanent ID

def get_trichy_movies():
    # Updated URL to fetch exactly 'Now Showing' movies using cat=MT
    target_url = "https://in.bookmyshow.com/explore/movies-trichy?cat=MT"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=stealth&render=true&wait=10000"
    
    # Dictionary to store Movie Name as Key and BookMyShow Link as Value
    movies_dict = {} 
    
    try:
        response = requests.get(proxy_url, timeout=60)
        
        if response.status_code == 200:
            if "Just a moment..." in response.text or "Cloudflare" in response.text:
                print("⚠️ ERROR: Blocked by BookMyShow Anti-bot (Cloudflare).")
                return {}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape movie titles AND their direct links
            for a in soup.find_all('a', href=True):
                href = a['href']
                
                # Check if the link is a valid BookMyShow movie link
                if 'ET00' in href and ('/movies/' in href or '/trichy/movies' in href):
                    title = ""
                    
                    # Try to get name from image alt tag
                    img = a.find('img')
                    if img and img.get('alt'):
                        title = img.get('alt').strip().upper()
                    else:
                        # Fallback to getting text from divs
                        texts = [div.get_text().strip().upper() for div in a.find_all('div') if div.get_text().strip()]
                        if texts:
                            title = texts[0]

                    # Filter and add to dictionary
                    if title and 2 < len(title) < 50:
                        blacklist = ["BOOKING", "TICKET", "WATCH", "CLICK", "OFFER", "LATEST", "BMS", "PROMOTED", "RUPEES"]
                        if not any(x in title for x in blacklist):
                            # Ensure link is absolute
                            full_link = f"https://in.bookmyshow.com{href}" if href.startswith('/') else href
                            movies_dict[title] = full_link
                            
        else:
            print(f"⚠️ Scraper Error: HTTP Status Code {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Network/Scraper Error: {e}")
        
    return movies_dict

def run_all():
    movies_data = get_trichy_movies()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *TRICHY MOVIES - NOW SHOWING* 🎬\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not movies_data:
        body = "⚠️ *Status:* No movies detected. (Possible API Block or Empty List)\n"
    else:
        body = ""
        # Sort movies alphabetically
        for m_name in sorted(movies_data.keys()):
            m_link = movies_data[m_name]
            body += f"✅ *{m_name}*\n🎟️ [Check Showtimes & Book Tickets]({m_link})\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n👉 [Explore All on BMS](https://in.bookmyshow.com/explore/movies-trichy?cat=MT)"
    final_msg = header + meta + body + footer

    user_list = [MY_ID]
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                extra_users = json.load(f)
                for u in extra_users:
                    if u not in user_list:
                        user_list.append(u)
            except: pass
            
    for user_id in user_list:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={
                    "chat_id": user_id, 
                    "text": final_msg, 
                    "parse_mode": "Markdown", 
                    "disable_web_page_preview": "true" # Keeps the message clean without huge image previews
                }
            )
        except Exception as e: 
            print(f"Telegram Error for {user_id}: {e}")

if __name__ == "__main__":
    run_all()
