#!/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# trading_core/portfolio_tracker.py

import json
from pathlib import Path
from datetime import datetime
from backend.globals import logger
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark

# === File Paths ===
PORTFOLIO_FILE = Path("data/portfolio.json")
HISTORY_FILE = Path("data/trade_history.jsonl")

# === Metadata ===
WATERMARK = "source:GremlinGPT"
ORIGIN = "portfolio_tracker"

PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)


# === Load/Save Helpers ===
def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_portfolio():
    return load_json(PORTFOLIO_FILE)


def save_portfolio(data):
    save_json(PORTFOLIO_FILE, data)
    inject_watermark(origin=ORIGIN)
    logger.info("[PORTFOLIO] Portfolio saved.")


# === Trade Logging ===
def log_trade(symbol, action, shares, price):
    event = {
        "symbol": symbol,
        "action": action,
        "shares": shares,
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "origin": ORIGIN,
        "watermark": WATERMARK,
    }

    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    logger.info(f"[PORTFOLIO] Trade logged: {event}")

    summary = f"{action.upper()} {shares} {symbol} @ ${price:.2f}"
    vector = embed_text(summary)

    package_embedding(
        text=summary,
        vector=vector,
        meta=event,
    )

    inject_watermark(origin=f"{ORIGIN}::trade")


# === Update Position ===
def update_position(symbol, price, shares, action="buy"):
    portfolio = load_portfolio()
    existing = portfolio.get(symbol, {"shares": 0, "price": 0.0})

    if action == "buy":
        total_shares = existing["shares"] + shares
        avg_price = (
            (existing["shares"] * existing["price"] + shares * price) / total_shares
            if total_shares > 0
            else price
        )
    elif action == "sell":
        total_shares = max(0, existing["shares"] - shares)
        avg_price = existing["price"] if total_shares > 0 else 0.0
    else:
        total_shares = shares
        avg_price = price

    portfolio[symbol] = {
        "price": round(avg_price, 2),
        "shares": total_shares,
        "last_updated": datetime.utcnow().isoformat(),
    }

    save_portfolio(portfolio)
    log_trade(symbol, action, shares, price)


# === Position Utilities ===
def get_position(symbol):
    return load_portfolio().get(symbol, {"price": 0.0, "shares": 0})


def calculate_unrealized(symbol, current_price):
    position = get_position(symbol)
    return round((current_price - position["price"]) * position["shares"], 2)


def get_portfolio_summary(current_prices: dict):
    portfolio = load_portfolio()
    summary = {}
    total_value = 0.0
    total_cost = 0.0

    for symbol, data in portfolio.items():
        current_price = current_prices.get(symbol, data["price"])
        shares = data["shares"]
        entry_price = data["price"]
        cost = shares * entry_price
        value = shares * current_price
        pnl = value - cost

        summary[symbol] = {
            "shares": shares,
            "entry_price": entry_price,
            "current_price": current_price,
            "value": round(value, 2),
            "pnl": round(pnl, 2),
            "last_updated": data.get("last_updated"),
        }

        total_value += value
        total_cost += cost

    summary["total"] = {
        "value": round(total_value, 2),
        "cost_basis": round(total_cost, 2),
        "unrealized_gain": round(total_value - total_cost, 2),
    }

    logger.info(
        f"[PORTFOLIO] Summary generated. Total value: ${summary['total']['value']:.2f}"
    )
    return summary
