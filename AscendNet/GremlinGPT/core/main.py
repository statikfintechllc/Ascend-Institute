from tools import web_scraper, data_analyzer, trade_executor
from core import decision_engine, error_handler

def run():
    try:
        portfolio = web_scraper.scrape_portfolio()
        market_signals = data_analyzer.analyze_market_data()

        for symbol, action in market_signals.items():
            if action in ["buy", "sell"]:
                decision = decision_engine.make_decision(f"Should I {action} {symbol}?")
                if "yes" in decision.lower():
                    quantity = portfolio.get(symbol, 0) * 0.1  # Trade 10% of holdings
                    trade_executor.execute_trade(symbol, action, quantity)
    except Exception as e:
        error_handler.log_exception(e)
