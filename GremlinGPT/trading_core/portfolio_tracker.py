import json
from pathlib import Path

PORTFOLIO_FILE = Path("data/portfolio.json")


def load_portfolio():
    if not PORTFOLIO_FILE.exists():
        return {}
    with open(PORTFOLIO_FILE) as f:
        return json.load(f)


def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)


def update_position(symbol, price, shares):
    portfolio = load_portfolio()
    portfolio[symbol] = {"price": price, "shares": shares}
    save_portfolio(portfolio)
