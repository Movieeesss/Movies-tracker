import asyncio
import requests
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

async def get_bms_data():
    movie_results = []
    async with async_playwright() as p:
        # Memory save panna browser-ah lightweight-ah launch panrom
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
        context = await browser.new_context(viewport={'width': 800, 'height': 600})
        page = await context.new_page()
        await stealth_async(page)

        # Target URL
        url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
        
        try:
            print("Loading BMS...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Showtimes load aaga 5 seconds wait
            await asyncio.sleep(5)
            
            # BMS layout check: Ippo irukura latest selector '.list'
            movie_elements = await page.query_selector_all('li.list')
            
            for movie in movie_elements:
                title_elem = await movie.query_selector('strong')
                name = await title_elem.inner_text() if title_elem else ""
                
                # Timings extraction
                time_elems = await movie.query_selector_all('a[data-session-id], .showtime-pill')
                times = [await t.inner_text() for t in time_elems]
                
                if name and times:
                    movie_results.append({"name": name.strip(), "times": list(dict.fromkeys(times))})

        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()
    return movie_results

def run_all():
    # Sync wrapper
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
        body += "💡 _BMS security high. Retrying next cycle._\n"
    else:
        body = ""
        for m in movies:
            body += f"🎥 *{m['name'].upper()}*\n🕒 {', '.join(m['times'])}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
