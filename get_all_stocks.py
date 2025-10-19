import requests
import pandas as pd

url = "https://www.nseindia.com/api/master-fo-symbols"  # This returns all FO (Futures & Options) stocks
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/market-data/live-equity-market",
}

# Start session
session = requests.Session()
session.get("https://www.nseindia.com", headers=headers)  # Necessary initial GET

response = session.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Filter & rename
    df = df[['symbol', 'name']]
    df.rename(columns={"symbol": "SYMBOL", "name": "NAME OF COMPANY"}, inplace=True)

    # Save to CSV
    df.to_csv("CLEANED_EQUITY_L.csv", index=False)
    print("✅ CLEANED_EQUITY_L.csv saved with latest NSE data.")
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
