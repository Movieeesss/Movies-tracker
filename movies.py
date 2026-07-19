import requests

API_KEY = "e8c9eac3-517e-4e74-aa41-5ab98dc3e139"
TARGET_URL = "https://in.bookmyshow.com/movies/trichy/jana-nayagan/buytickets/ET00430817/20260724"
# Explicitly added js=true and increased wait time to 15 seconds for heavy JS loading
proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={TARGET_URL}&proxy=stealth&js=true&wait=15000"

print("Fetching data from BookMyShow...")
try:
    response = requests.get(proxy_url, timeout=60)
    
    if response.status_code == 200:
        # Check if the theater names actually exist in the raw response
        if "Cauvery" in response.text or "BHELEC" in response.text:
            print("✅ SUCCESS: Theaters FOUND in the raw HTML! (BeautifulSoup logic la thaan issue)")
        else:
            print("❌ FAILED: Theaters NOT FOUND! (WebScraping.ai JS render aagala, empty skeleton page thaan varudhu)")
            
        # Save the exact output to see what the bot is seeing
        with open("debug_bms.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("📁 File saved as 'debug_bms.html'. Chrome-la open panni parunga, page empty-a iruka nu theriyum.")
        
    else:
        print(f"⚠️ API Error: Status {response.status_code}")
except Exception as e:
    print(f"⚠️ Network Error: {e}")
