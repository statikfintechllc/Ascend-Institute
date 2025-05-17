import os
import logging

LOG_DIR = '/mnt/SkylineX/AscendAI/logs'
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'agent_trader.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

portfolio = {"USD": 10000}

def trade(stock, quantity, price):
    total = quantity * price
    if portfolio["USD"] >= total:
        portfolio["USD"] -= total
        logging.info(f"Bought {quantity} of {stock} at ${price:.2f} each. Remaining: ${portfolio['USD']:.2f}")
    else:
        logging.warning(f"Insufficient funds for {quantity} of {stock} at ${price:.2f}")

if __name__ == "__main__":
    logging.info("AgentTrader initialized.")
    try:
        trade("TSLA", 10, 123.45)
    except Exception as e:
        logging.exception("Trade execution failed. Blame the markets.")