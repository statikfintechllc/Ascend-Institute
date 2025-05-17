# tools/analyze_market_data.py

import pandas as pd
import ta
from memory.sqlite_memory import log_memory

def analyze_market_data(input_data):
    """
    input_data: dict with 'symbol': str, and 'prices': List[dict] like:
    [
        {"timestamp": ..., "open": ..., "high": ..., "low": ..., "close": ..., "volume": ...},
        ...
    ]
    Returns:
        dict with indicator values and signal
    """
    symbol = input_data.get("symbol", "UNKNOWN")
    prices = input_data.get("prices")

    if not prices or len(prices) < 30:
        return {"error": "Insufficient price data for analysis."}

    df = pd.DataFrame(prices)
    df = df.sort_values(by="timestamp")
    df.set_index("timestamp", inplace=True)

    # Calculate indicators
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["sma_20"] = ta.trend.SMAIndicator(df["close"], window=20).sma_indicator()

    latest = df.iloc[-1]

    # Decision logic
    signal = "hold"
    if latest["rsi"] < 30 and latest["macd"] > latest["macd_signal"]:
        signal = "buy"
    elif latest["rsi"] > 70 and latest["macd"] < latest["macd_signal"]:
        signal = "sell"

    # Log it
    summary = {
        "symbol": symbol,
        "close": round(latest["close"], 2),
        "rsi": round(latest["rsi"], 2),
        "macd": round(latest["macd"], 4),
        "macd_signal": round(latest["macd_signal"], 4),
        "sma_20": round(latest["sma_20"], 2),
        "signal": signal
    }

    log_memory(f"Market Analysis for {symbol}", str(summary), tag="market_analysis")

    return summary
