# Ascend_PennyHunter.py
import yfinance as yf
import json
from datetime import datetime

WATCHLIST = ["GNS", "SNTI", "AVCT", "TOP", "HCDI"]
THRESHOLD = 0.07  # 7% premarket gain trigger

def scan_runners():
    ghost_hits = []
    for ticker in WATCHLIST:
        data = yf.Ticker(ticker).history(period="1d", interval="5m")
        if len(data) < 2:
            continue
        open_price = data["Open"][0]
        last_price = data["Close"][-1]
        change = (last_price - open_price) / open_price
        if change >= THRESHOLD:
            ghost_hits.append({
                "ticker": ticker,
                "change": f"{change*100:.2f}%",
                "time": str(datetime.now()),
                "phantom": True
            })
    with open("phantom_yield.json", "w") as f:
        json.dump(ghost_hits, f, indent=2)

if __name__ == "__main__":
    scan_runners()