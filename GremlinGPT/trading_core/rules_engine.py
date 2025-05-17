def apply_signal_rules(stock):
    if stock["price"] > stock["ema"] and stock["price"] > stock["vwap"]:
        return {"signal": "Breakout"}
    elif stock["volume"] > 100000:
        return {"signal": "Watch"}
    else:
        return None

