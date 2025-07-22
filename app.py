import streamlit as st
from stock_data import get_stock_data
from news_scraper import get_news
from sentiment_analysis import analyze_sentiment
import pandas as pd
import matplotlib.pyplot as plt

# Sample stock list (You can expand this)
INDIAN_STOCKS = {
    "Tata Steel": "TATASTEEL.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS"
}


st.set_page_config(page_title="Stock Market Sentiment Analyzer", layout="centered")
st.title("📊 Stock Market Sentiment Analyzer")

# Input from user
selected_stock = st.selectbox("Select a Stock:", list(INDIAN_STOCKS.keys()))
ticker = INDIAN_STOCKS[selected_stock]


if ticker:
    # Fetch stock price data
    st.subheader("📈 Stock Price (Last 7 Days)")
    try:
        stock_data = get_stock_data(ticker)
        st.line_chart(stock_data['Close'])
    except Exception as e:
        st.error(f"Failed to fetch stock data: {e}")

    # Fetch news and analyze sentiment
    st.subheader("📰 Latest News Headlines & Sentiment")
    try:
        headlines = get_news(ticker)
        if headlines:
            sentiment_results = analyze_sentiment(headlines)
            df = pd.DataFrame(sentiment_results, columns=["Headline", "Sentiment Score"])
            st.dataframe(df)

            st.subheader("📊 Sentiment Score Distribution")
            plt.figure(figsize=(6, 3))
            plt.hist(df["Sentiment Score"], bins=10, color="skyblue", edgecolor="black")
            plt.xlabel("Sentiment Score")
            plt.ylabel("Number of Headlines")
            st.pyplot(plt)
        else:
            st.warning("No recent news articles found.")
    except Exception as e:
        st.error(f"Error fetching or analyzing news: {e}")
