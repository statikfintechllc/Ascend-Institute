# Fractal Echo AutoBot v1.1 - Full Autonomous Mode
# Requires: yfinance, pandas, numpy, matplotlib, ta, requests, bs4, psutil, pyautogui, selenium

import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import MACD
from ta.momentum import RSIIndicator
from bs4 import BeautifulSoup
import requests
import psutil
import datetime
import time
# import pyautogui  # Uncomment if using GUI automation
# from selenium import webdriver  # Uncomment if using Selenium

SYMBOLS = ["SPY", "IWM"]
TIMEFRAME = "5m"
LOOKBACK_DAYS = 10

def download_data(symbol, period="10d", interval="5m"):
    df = yf.download(symbol, period=period, interval=interval)
    df.dropna(inplace=True)
    df["MACD"] = MACD(df["Close"]).macd_diff()
    df["RSI"] = RSIIndicator(df["Close"]).rsi()
    return df

def find_fractals(df):
    fractals = []
    for i in range(50, len(df)-50):
        window = df.iloc[i-10:i+10]
        if (
            window["RSI"].iloc[-1] < 60 and
            window["MACD"].iloc[-1] < 0 and
            window["Close"].iloc[-1] < window["Close"].max() - 1
        ):
            fractals.append(i)
    return fractals

def alert_logic(df, fractals):
    latest = df.iloc[-1]
    for idx in fractals:
        echo = df.iloc[idx]
        if (
            abs(echo["RSI"] - latest["RSI"]) < 2 and
            abs(echo["MACD"] - latest["MACD"]) < 0.2
        ):
            print(f"[ECHO MATCH DETECTED] near {latest.name}")
            return True
    return False

def scrape_finviz():
    print("Scraping Finviz for penny stock gainers...")
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_price_u5&ft=4"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    tickers = []
    for row in soup.find_all('a', class_='screener-link-primary'):
        tickers.append(row.text)
    print(f"Penny stock gainers: {tickers}")
    return tickers

def map_cpu():
    print("Mapping CPU usage by process:")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            print(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def run_autobot():
    for symbol in SYMBOLS:
        df = download_data(symbol)
        fractals = find_fractals(df)
        match = alert_logic(df, fractals)
        if match:
            print(f">>> ALERT: {symbol} fractal echo matching NOW <<<")
    scrape_finviz()
    map_cpu()

if __name__ == "__main__":
    run_autobot()
