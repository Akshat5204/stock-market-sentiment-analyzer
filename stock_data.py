import yfinance as yf

def get_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)
