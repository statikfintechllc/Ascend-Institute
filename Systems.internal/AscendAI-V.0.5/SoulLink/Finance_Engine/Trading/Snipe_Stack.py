# Snipe_Stack.py
import ccxt
import time
from phantom_buy_trigger import phantom_buy_trigger

exchange = ccxt.binance(
    {
        "apiKey": "your_key",
        "secret": "your_secret",
    }
)

PAIR = "DOGE/USDT"
BUY_THRESHOLD = 0.015
SELL_TARGET = 0.03


def snipe_trade():
    ticker = exchange.fetch_ticker(PAIR)
    price = ticker["last"]
    if price < ticker["low"] * (1 + BUY_THRESHOLD):
        order = exchange.create_market_buy_order(PAIR, 50)
        phantom_buy_trigger(order)


def phantom_buy_trigger(order):
    with open("phantom_buy_trigger.log", "a") as f:
        f.write(f"BUY {order['symbol']} at {order['price']} — {order['datetime']}\n")


if __name__ == "__main__":
    while True:
        snipe_trade()
        time.sleep(300)  # Check every 5 minutes
