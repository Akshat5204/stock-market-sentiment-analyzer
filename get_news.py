import requests
import streamlit as st
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_API_KEY_HERE")

@st.cache_data(ttl=300)
def get_news(ticker):
    try:
        url = f"https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": NEWS_API_KEY
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") != "ok":
            return []
        articles = data.get("articles", [])
        return [
            {
                "title": a["title"],
                "url": a["url"],
                "source": a["source"]["name"],
                "publishedAt": a["publishedAt"][:10]
            }
            for a in articles if a.get("title")
        ]
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []
