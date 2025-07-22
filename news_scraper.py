# news_scraper.py

import requests
from bs4 import BeautifulSoup

def get_news(query, max_headlines=5):
    url = f"https://www.bing.com/news/search?q={query}+stock&FORM=HDRSC6"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for item in soup.find_all("a", {"class": "title"}, limit=max_headlines):
        title = item.get_text()
        if title:
            headlines.append(title.strip())

    return headlines
