import random
import math
from datetime import datetime
from backend.globals import logger

WATERMARK = "source:GremlinGPT"
ORIGIN = "stock_scraper"

# Simulated stock universe (can be expanded or tied to live API)
PENNY_UNIVERSE = [
    "BBIG",
    "GNS",
    "MULN",
    "CEI",
    "COSM",
    "SNDL",
    "ZOM",
    "TRKA",
    "NILE",
    "AITX",
]


def simulate_technical_indicators(price, volatility):
    """
    Generate mock indicators based on price movement and volatility
    """
    drift = random.uniform(-0.03, 0.03) * volatility
    ema = round(price * (1 - drift), 3)
    vwap = round((price + ema + random.uniform(-0.02, 0.02)) / 2, 3)

    # RSI logic: overbought (>70), oversold (<30)
    rsi = round(random.uniform(25, 80), 2)

    # MACD: price vs signal line difference
    macd = round((price - ema) + random.uniform(-0.1, 0.1), 3)

    return ema, vwap, rsi, macd


def get_live_penny_stocks(limit=6):
    """
    Simulated scanner: returns `limit` penny stock dicts w/ enhanced features.
    """
    selected = random.sample(PENNY_UNIVERSE, limit)
    results = []

    for symbol in selected:
        base = round(random.uniform(0.10, 4.00), 2)
        volatility = round(random.uniform(0.05, 0.35), 2)

        price = round(base + random.uniform(-0.25, 0.25), 2)
        volume = random.randint(100_000, 5_000_000)

        ema, vwap, rsi, macd = simulate_technical_indicators(price, volatility)

        stock_data = {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "ema": ema,
            "vwap": vwap,
            "rsi": rsi,
            "macd": macd,
            "volatility": volatility,
            "timestamp": datetime.utcnow().isoformat(),
        }

        logger.debug(
            f"[SCRAPER] Mocked stock data: {symbol} @ ${price} (Vol: {volume})"
        )
        results.append(stock_data)

    return results
