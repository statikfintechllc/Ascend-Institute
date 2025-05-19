import random


def get_live_penny_stocks():
    return [
        {
            "symbol": "BBIG",
            "price": round(random.uniform(0.5, 0.9), 2),
            "volume": 900000,
            "ema": 0.6,
            "vwap": 0.62,
        },
        {
            "symbol": "GNS",
            "price": 1.75,
            "volume": 2000000,
            "ema": 1.65,
            "vwap": 1.70,
        },
        {
            "symbol": "MULN",
            "price": 0.23,
            "volume": 450000,
            "ema": 0.20,
            "vwap": 0.22,
        },
    ]
