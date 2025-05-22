from tools import web_scraper, data_analyzer, trade_executor
from core import decision_engine, error_handler
from multiprocessing import Process
import subprocess


def run_dashboard_server():
    subprocess.run(["python", "mobile_dashboard/dashboard_server.py"])


def run_visual_dashboard():
    subprocess.run(["python", "mobile_dashboard/dashboard.py"])


if __name__ == "__main__":
    p1 = Process(target=run_dashboard_server)
    p2 = Process(target=run_visual_dashboard)

    p1.start()
    p2.start()

    p1.join()
    p2.join()


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
