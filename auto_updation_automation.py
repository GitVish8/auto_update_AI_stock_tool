import os
import sys
import requests
import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol):
    """
    Fetch historical stock data and basic company information using yfinance.
    """
    print(f"Fetching data for {symbol}...")
    ticker_data = yf.Ticker(symbol)  # Renamed local variable
    hist = ticker_data.history(period="1y")
    hist = pd.DataFrame(hist)
    info = ticker_data.info

    fundamentals = {
        "Ticker": symbol,
        "Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "Trailing P/E": info.get("trailingPE", "N/A"),
        "Forward P/E": info.get("forwardPE", "N/A"),
        "Debt-to-Equity": info.get("debtToEquity", "N/A"),
        "Return on Equity": info.get("returnOnEquity", "N/A"),
    }
    return hist, fundamentals

def self_update(update_url):
    """
    Automatically writes new code updates into the script.
    """
    script_path = os.path.abspath(__file__)
    backup_path = script_path + ".backup"
    try:
        with open(script_path, "r") as original_script:
            current_code = original_script.read()
        with open(backup_path, "w") as backup_script:
            backup_script.write(current_code)

        print("Checking for updates...")
        response = requests.get(update_url)  # Renamed parameter
        if response.status_code == 200:
            new_code = response.text
            with open(script_path, "w") as updated_script:
                updated_script.write(new_code)
            print("Update applied successfully. Restarting...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            print(f"Failed to fetch updates. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to update the program: {e}")

if __name__ == "__main__":
    ticker = "TATAMOTORS.BO"
    hist_data, company_fundamentals = fetch_stock_data(ticker)
    hist_data.to_csv(f"{ticker}_analyzed.csv", index=True)
    print("Company Fundamentals:")
    for key, value in company_fundamentals.items():
        print(f"{key}: {value}")

    # Auto-update
    repo_url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/your_script.py"
    self_update(repo_url)
