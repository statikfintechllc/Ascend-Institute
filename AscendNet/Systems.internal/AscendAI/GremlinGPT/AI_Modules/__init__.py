from tools.scrape_web import scrape_web
from tools.query_api import query_api
from tools.buy_crypto import buy_crypto           # Sim/API-based crypto trader
from tools.self_edit import self_edit
from tools.robinhood_trade import robinhood_trade  # Web scraper-based trader
from tools.analyze_market_data import analyze_market_data

tool_registry = {
    "scrape_web": scrape_web,
    "analyze_market_data": analyze_market_data,
    "query_api": query_api,
    "buy_crypto": buy_crypto, # Usage: "buy_crypto {'symbol': 'BTCUSDT', 'amount': 0.01}"
    "self_edit": self_edit,
    "robinhood_trade": robinhood_trade, # Usage: "robinhood_trade {'symbol': 'BTC'}"
}
