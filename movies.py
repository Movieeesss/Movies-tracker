import asyncio
import requests
import os
from playwright.async_api import async_playwright
from playwright_stealth import stealth 
from datetime import datetime, timedelta

# Bot Settings
TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

async def get_bms_data():
    # Render-la browser executable missing aagaama irukka force install
    print("Checking/Installing Chromium browser...")
    os.system("playwright install chromium")

    movie_results = []
    async with async_playwright() as p:
        # Optimized for Low RAM (512MB)
        browser = await p.chromium.launch(
            headless=True, 
            args=[
                "--no-sandbox", 
                "--disable-setuid-sandbox", 
                "--disable-dev-shm-usage",
                "--single-process",        # Low memory-kku ithu romba mukkiyam
                "--disable-gpu",           # GPU thevai illai
                "--disable-extensions"     # Extensions disable panni RAM-ah save panrom
            ]
        )
        
        # Viewport size-ah kuraichu browser load-ah reduce panrom
        context = await browser.new_context(
            viewport={'width': 800, 'height': 600},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        await stealth(page)

        # Target URL: LA Cinemas Maris Trichy (April 2nd)
        url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
        
        try:
            print(f"Navigating to: {url}")
            # Networkidle vara wait pannuna RAM exceed aagalaam, so domcontentloaded best
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            
            # Browser render aaga Render-la konjam extra time (20s) kodukkuroom
            print("Waiting 20 seconds for page rendering...")
            await asyncio.sleep(20)
            
            # Trigger JavaScript for showtimes
            await page.mouse.wheel(0, 600)
            await asyncio.sleep(5)

            # Movie list extraction
            movie_elements = await page.query_selector_all('li.list')
            print(f"Found {len(movie_elements)} movies on page.")
            
            for movie in movie_elements:
                # Name extraction
                title_elem = await movie.query_selector('strong')
                name = await title_elem.inner_text() if title_elem else ""
                
                # Timing extraction
                time_elems = await movie.query_selector_all('a[data-session-id], .showtime-pill, .__showtime')
                times = []
                for t in time_elems:
                    t_text = await t.inner_text()
                    if ":" in t_text:
                        times.append(t_text.strip())
                
                if name and times:
                    movie_results.append({
                        "name": name.strip().upper(), 
                        "times": list(dict.fromkeys(times))
                    })

        except Exception as e:
            print(f"SCRAPING ERROR: {e}")
            # Error vanthaal bot-kku notification anuppum
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         params={"chat_id": CHAT_ID, "text": f"❌ Scraper Error: {e}"})
        
        finally:
            await browser.close()
            
    return movie_results

def run_all():
    # Trigger Start Message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "⏳ Scraper started... fetching data from BMS.", "parse_mode": "Markdown"})
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    movies = loop.run_until_complete(get_bms_data())
    
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🎬 *LA CINEMAS (MARIS) - LIVE UPDATES* 🎬\n"
    meta = f"📅 *DATE:* 02-04-2026\n🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not movies:
        body = "📊 *Status:* Theater syncing live timings...\n"
        body += "💡 _BMS security high or shows not opened yet._\n"
    else:
        body = ""
        for m in movies:
            body += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    
    # Final Result Telegram-ku anuppuvom
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
