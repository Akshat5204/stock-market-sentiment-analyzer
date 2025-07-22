# stock_data.py

import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    data = yf.download(ticker, start=start_date, end=end_date)
    return data
