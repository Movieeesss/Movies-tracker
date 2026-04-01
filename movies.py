import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TOKEN = "8745585993:AAE2zRpimM9_VW9YK0I7FhDmvHb7iy1tw9A"
CHAT_ID = "1115358053"

def get_google_live_timings():
    # Google-la search panna timings varum
    url = "https://www.google.com/search?q=LA+Cinemas+Maris+Trichy+show+timings&hl=en"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    movie_list = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google-oda movie timing card extraction logic
        # Indha section website-ku website maarum, so simple-ah name and time-ah check panrom
        for block in soup.find_all('div', attrs={'data-attrid': 'kc:/film/film:showtimes'}):
            name = block.find('div', class_='BNeaW').text if block.find('div', class_='BNeaW') else "Movie"
            times = [t.text for t in block.find_all('div', class_='S3ne9e') if ":" in t.text]
            if name and times:
                movie_list.append({"name": name, "times": times})
        return movie_list
    except:
        return []

# Baaki send logic adhe dhaan...
