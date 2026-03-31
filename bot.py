import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Steel bot updates-ku unga pazhaya bot token use pannikonga
TOKEN = "8754915572:AAG6r3jr7h1xXHeCZ4HYJ-6I8uGLnFPo7Vw"
CHAT_ID = "1115358053"

def get_steel_prices():
    url = "https://ammantry.com/products/tmt/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    prices = {"8mm": 58.0, "10-25mm": 57.0} # Fallback prices
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        # Website-la irukka price-ah exact-ah filter panrom
        m8 = re.search(r"8mm\s*–\s*₹(\d+)", page_text)
        mothers = re.search(r"10-25\s*mm\s*–\s*₹(\d+)", page_text)

        if m8: prices["8mm"] = float(m8.group(1))
        if mothers: prices["10-25mm"] = float(mothers.group(1))
        
        return prices
    except:
        return prices

def send_update():
    try:
        data = get_steel_prices()
        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        now_time = ist_now.strftime("%I:%M %p")
        
        message = f"🎯 *5-MIN STEEL TRACKER* 🎯\n"
        message += f"🕒 Time: {now_time} (IST)\n"
        message += "━━━━━━━━━━━━━━━━━━━━\n"
        message += f"📏 8mm   : ₹{data['8mm']:.2f} / kg\n"
        message += f"📏 10mm  : ₹{data['10-25mm']:.2f} / kg\n"
        message += f"📏 16mm  : ₹{data['10-25mm']:.2f} / kg\n"
        message += f"📏 20mm  : ₹{data['10-25mm']:.2f} / kg\n"
        message += f"📏 25mm  : ₹{data['10-25mm']:.2f} / kg\n"
        message += "━━━━━━━━━━━━━━━━━━━━\n"
        message += "✅ *Live from ammantry.com*"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        print(f"Success: Steel price sent at {now_time}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_update()
