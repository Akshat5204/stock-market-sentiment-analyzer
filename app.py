# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as px
from sentiment_analysis import analyze_sentiment
from news_scraper import get_news



# Dark/Light Mode Toggle (GFG-style)
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

toggle = st.button("🌓 Theme")

if toggle:
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# Apply the theme
if st.session_state["theme"] == "dark":
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #1e1e1e;
                color: #f1f1f1;
            }
            .stButton>button {
                background-color: #444;
                color: white;
            }
            .stSelectbox, .stTextInput, .stDataFrame, .stSlider {
                background-color: #2b2b2b;
                color: #f1f1f1;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .stButton>button {
                background-color: #ddd;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

# Set up the Streamlit page
st.set_page_config(page_title="📊 Stock Market Sentiment Analyzer", layout="wide")
# Theme-aware label colors for dropdowns and widgets
st.markdown(
    """
    <style>
    /* Force labels to be visible in both dark and light mode */
    label, .stSelectbox label, .stDateInput label {
        color: black !important;  /* Light mode default */
    }
    [data-theme="dark"] label, [data-theme="dark"] .stSelectbox label, [data-theme="dark"] .stDateInput label {
        color: white !important;  /* Dark mode default */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Stock Market Sentiment Analyzer")

# Load stock list
try:
    df_stocks = pd.read_csv("CLEANED_EQUITY_L.csv")

    # Check for expected columns
    if "SYMBOL" not in df_stocks.columns or "NAME OF COMPANY" not in df_stocks.columns:
        raise ValueError("Missing required columns in CSV.")

    # Create dictionary for dropdown
    stock_dict = dict(zip(df_stocks["NAME OF COMPANY"], df_stocks["SYMBOL"] + ".NS"))

    # Show preview in sidebar
    with st.sidebar:
        st.markdown("### 📄 CSV Preview")
        st.dataframe(df_stocks)

    # Stock selection
    selected_stock = st.selectbox("Select a Stock:", list(stock_dict.keys()))
    ticker = stock_dict[selected_stock]

except Exception as e:
    st.error(f"⚠️ Error loading stocks: {e}")
    st.stop()

# Time range options
TIME_RANGES = {
    "1 Day": ("1d", "5m"),
    "1 Month": ("1mo", "1d"),
    "1 Year": ("1y", "1wk"),
    "5 Years": ("5y", "1mo"),
    "Max (All Time)": ("max", "3mo")
}

selected_range = st.selectbox("Select Time Range:", list(TIME_RANGES.keys()))
period, interval = TIME_RANGES[selected_range]

# Plot stock price chart
st.subheader(f"📈 Price Chart for {selected_stock} ({selected_range})")
try:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    if hist.empty:
        raise ValueError("No historical data available.")
    st.line_chart(hist["Close"])
except Exception as e:
    st.error(f"Failed to fetch stock data: {e}")

# News and Sentiment
st.subheader("📰 News Sentiment Analysis")
try:
    headlines = get_news(ticker)
    if headlines:
        sentiment_results = analyze_sentiment(headlines)
        df_sentiment = pd.DataFrame(sentiment_results, columns=["Headline", "Sentiment Score", "Sentiment Label"])

        st.dataframe(df_sentiment)

        # Histogram
        st.subheader("📊 Sentiment Score Distribution")
        plt.figure(figsize=(6, 3))
        plt.hist(df_sentiment["Sentiment Score"], bins=10, color="skyblue", edgecolor="black")
        plt.xlabel("Sentiment Score")
        plt.ylabel("Number of Headlines")
        st.pyplot(plt)

        # Pie Chart
        st.subheader("🧠 Sentiment Breakdown")
        sentiment_counts = df_sentiment["Sentiment Label"].value_counts()
        st.plotly_chart(px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="News Sentiment Breakdown",
            hole=0.3
        ))

        # Overall Score
        # Overall Score
        avg_score = df_sentiment["Sentiment Score"].mean()

        # Theme-aware sentiment display
        if avg_score > 0.05:
            sentiment_text = f"📈 Overall Sentiment: Positive ({avg_score:.2f})"
            color = "#4CAF50" if st.session_state["theme"] == "light" else "#81C784"
        elif avg_score < -0.05:
            sentiment_text = f"📉 Overall Sentiment: Negative ({avg_score:.2f})"
            color = "#E53935" if st.session_state["theme"] == "light" else "#EF9A9A"
        else:
            sentiment_text = f"⚖️ Overall Sentiment: Neutral ({avg_score:.2f})"
            color = "#FF9800" if st.session_state["theme"] == "light" else "#FFB74D"

        st.markdown(
            f"<div style='padding:10px; border-radius:5px; background-color:rgba(0,0,0,0); "
            f"color:{color}; font-weight:bold; font-size:18px;'>{sentiment_text}</div>",
            unsafe_allow_html=True
        )

    else:
        st.warning("No recent news found.")
except Exception as e:
    st.error(f"Error fetching or analyzing news: {e}")
