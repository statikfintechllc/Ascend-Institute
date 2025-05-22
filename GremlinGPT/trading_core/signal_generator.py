from trading_core.rules_engine import apply_signal_rules
from trading_core.stock_scraper import get_live_penny_stocks
from memory.vector_store.embedder import package_embedding, embed_text, inject_watermark
from backend.globals import logger
from datetime import datetime

WATERMARK = "source:GremlinGPT"
ORIGIN = "signal_generator"


def generate_signals():
    stocks = get_live_penny_stocks()
    signals = []

    for stock in stocks:
        signal = apply_signal_rules(stock)
        if signal:
            result = {**stock, **signal}
            signals.append(result)

            summary = (
                f"{stock['symbol']} @ ${stock['price']:.2f} | "
                f"Signal: {', '.join(signal['signal'])}"
            )

            vector = embed_text(summary)

            package_embedding(
                text=summary,
                vector=vector,
                meta={
                    "symbol": stock["symbol"],
                    "signal": signal["signal"],
                    "price": stock["price"],
                    "ema": stock.get("ema"),
                    "vwap": stock.get("vwap"),
                    "rsi": stock.get("rsi"),
                    "volume": stock.get("volume"),
                    "timestamp": datetime.utcnow().isoformat(),
                    "origin": ORIGIN,
                    "watermark": WATERMARK,
                },
            )

            logger.info(f"[SIGNAL] {summary}")
            inject_watermark(origin=ORIGIN)

    return signals
