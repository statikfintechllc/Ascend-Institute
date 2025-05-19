from trading_core.rules_engine import apply_signal_rules
from trading_core.stock_scraper import get_live_penny_stocks
from memory.vector_store.embedder import package_embedding
from loguru import logger


def generate_signals():
    stocks = get_live_penny_stocks()
    signals = []

    for stock in stocks:
        signal = apply_signal_rules(stock)
        if signal:
            result = {**stock, **signal}
            signals.append(result)

            text = f"{stock['symbol']} @ ${stock['price']} | Signal: {signal['signal']}"
            vec = [
                stock["price"],
                stock["ema"],
                stock["vwap"],
                stock["volume"],
            ]
            package_embedding(
                text=text,
                vector=vec,
                meta={"origin": "signal_scan", "type": "trading_signal"},
            )
            logger.info(f"[SIGNAL] {text}")
    return signals
