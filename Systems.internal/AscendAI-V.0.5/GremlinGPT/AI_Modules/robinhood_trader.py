import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from memory.sqlite_memory import log_memory
import ta

# Load environment credentials
ROBINHOOD_EMAIL = os.getenv("ROBINHOOD_EMAIL")
ROBINHOOD_PASSWORD = os.getenv("ROBINHOOD_PASSWORD")

# Init headless browser
def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


# Perform Robinhood login
def login_robinhood(driver):
    driver.get("https://robinhood.com/login")
    time.sleep(3)
    driver.find_element(By.NAME, "username").send_keys(ROBINHOOD_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(ROBINHOOD_PASSWORD + Keys.RETURN)
    time.sleep(5)
    logging.info("[Robinhood] Login attempted.")


# Scrape portfolio value
def get_portfolio_value(driver):
    driver.get("https://robinhood.com/account")
    time.sleep(4)
    try:
        elem = driver.find_element(By.CLASS_NAME, "PortfolioBalance__StyledBalance")
        value = elem.text.replace("$", "").replace(",", "")
        return float(value)
    except Exception as e:
        logging.error(f"[Robinhood] Portfolio scrape failed: {e}")
        return 0


# Position sizing
def calculate_trade_size(portfolio_value, pct=1.0):
    return round(portfolio_value * (pct / 100), 2)


# Basic RSI + MACD trading logic
def analyze_market(symbol):
    prices = [100 + i for i in range(60)]  # Replace with real prices later
    df = pd.DataFrame({"close": prices})
    rsi = ta.momentum.RSIIndicator(df["close"]).rsi().iloc[-1]
    macd = ta.trend.MACD(df["close"]).macd().iloc[-1]

    if rsi < 30 and macd > 0:
        return "buy"
    elif rsi > 70 and macd < 0:
        return "sell"
    return "hold"


# "Execute" trade via scraping (currently logs only)
def execute_trade(driver, symbol, action, amount):
    driver.get(f"https://robinhood.com/stocks/{symbol}")
    time.sleep(3)
    logging.info(f"[TRADE] {action.upper()} {symbol} — ${amount}")
    log_memory(f"{action.upper()} {symbol}", f"Amount: ${amount}", tag="trading")


# GremlinGPT-callable function
def robinhood_trade(input_data=None):
    symbol = "BTC"  # default
    if input_data and isinstance(input_data, dict) and "symbol" in input_data:
        symbol = input_data["symbol"].upper()

    driver = init_driver()

    try:
        login_robinhood(driver)
        portfolio = get_portfolio_value(driver)
        size = calculate_trade_size(portfolio)
        signal = analyze_market(symbol)

        if signal in ["buy", "sell"]:
            execute_trade(driver, symbol, signal, size)
            return f"[AI TRADE] {signal.upper()} {symbol} — ${size}"
        else:
            return "[AI TRADE] HOLD — No trade this cycle."

    except Exception as e:
        logging.error(f"[Robinhood] Fatal error: {e}")
        return f"[ERROR] {e}"

    finally:
        driver.quit()
