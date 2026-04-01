import asyncio
import requests
from playwright.async_api import async_playwright
from playwright_stealth import stealth 
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

async def get_bms_data():
    # TEST MESSAGE: Scraper start aana udane ithu varanum
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "⏳ Scraper started... fetching data from BMS.", "parse_mode": "Markdown"})

    movie_results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(viewport={'width': 800, 'height': 600})
        page = await context.new_page()
        await stealth(page)

        url = "https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402"
        
        try:
            print(f"Opening: {url}")
            await page.goto(url, wait_until="networkidle", timeout=90000)
            
            # INCREASED WAIT: 15 seconds for slow Render server
            print("Waiting 15 seconds for showtimes...")
            await asyncio.sleep(15)
            
            await page.mouse.wheel(0, 600)
            await asyncio.sleep(3)

            movie_elements = await page.query_selector_all('li.list')
            print(f"Found {len(movie_elements)} movies.")
            
            for movie in movie_elements:
                title_elem = await movie.query_selector('strong')
                name = await title_elem.inner_text() if title_elem else ""
                
                time_elems = await movie.query_selector_all('a[data-session-id], .showtime-pill')
                times = [await t.inner_text() for t in time_elems if ":" in await t.inner_text()]
                
                if name and times:
                    movie_results.append({"name": name.strip().upper(), "times": list(dict.fromkeys(times))})

        except Exception as e:
            print(f"SCRAPING ERROR: {e}")
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         params={"chat_id": CHAT_ID, "text": f"❌ Scraper Error: {e}"})
        
        await browser.close()
    return movie_results

def run_all():
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
        body += "💡 _BMS might be blocking or page didn't load in time._\n"
    else:
        body = ""
        for m in movies:
            body += f"🎥 *{m['name']}*\n🕒 {', '.join(m['times'])}\n\n"
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n🎟️ [Book on BMS](https://in.bookmyshow.com/buytickets/la-cinemas-maris-trichy/cinema-trich-LATG-MT/20260402)"
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": header + meta + body + footer, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_all()
