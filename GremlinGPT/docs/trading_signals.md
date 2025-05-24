<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-red?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

# Trading Signals — GremlinGPT v1.0.2 (v4)

---

## Overview

The `trading_core/` subsystem is a modular, offline engine designed for **penny stock discovery, analysis, and signal generation**. It runs autonomously, writes to memory, and directly influences planning and retraining loops.

The goal is to create **precise, explainable, and actionable market signals** under $10 USD per share, enriched with embedded metadata and confidence scores.

---

## Modules

| File                     | Description                                        |
|--------------------------|----------------------------------------------------|
| `signal_generator.py`    | Detects trade signals using rule-based heuristics  |
| `stock_scraper.py`       | Retrieves live stock data (offline, simulated, or live) |
| `rules_engine.py`        | Applies pattern logic (EMA, VWAP, volume)          |
| `portfolio_tracker.py`   | Stores and tracks position memory                  |
| `tax_estimator.py`       | Estimates capital gains on trades (US-compliant)   |

---

## Pipeline Flow

[stock_scraper.py]
↓
[rules_engine.py]
↓
[signal_generator.py]
↓
[embedder.py → memory vector store]

---

## Signal Detection Logic

Signals are triggered when:

- **Price < $10.00 USD**
- **EMA crossover (e.g. EMA5 > EMA20)**
- **VWAP gap-up or premarket breakout**
- **Volume > configured threshold**
- **NLP/sentiment boost via memory correlation**

Each signal object looks like:

```json
{
  "symbol": "PLTR",
  "type": "vwap_gap_up",
  "price": 7.45,
  "volume": 9320000,
  "confidence": 0.81,
  "timestamp": "2025-05-18T13:22:00Z"
}
```

Signal confidence is derived from weighted factors:
	•	Price trend
	•	Volume percentile
	•	Time-of-day heuristics
	•	NLP reinforcement if matched via scrape memory

⸻

## Embedding Signals Into Memory

Signals are embedded through the vector pipeline:
	1.	semantic_score.py — Vectorization (MiniLM)
	2.	package_embedding() — Stores vector + metadata
	3.	Stored in memory/vector_store/faiss/ or Chroma backend

Metadata sample:
```json
{
  "type": "signal",
  "strategy": "EMA_crossover",
  "source": "trading_core",
  "agent_id": "planner001",
  "timestamp": "2025-05-18T13:22:00Z"
}
```

Accessible via:
	•	MemoryGraph (frontend dashboard)
	•	planner_agent.py (for next-task generation)
	•	generate_dataset.py (training corpus)

⸻

Real-Time Refresh

Frontend: TradingPanel.js
	•	Polls signals every 0.2s via WebSocket (configurable)
	•	Auto-refreshes embedded task graph and stock list
	•	Color-coded by confidence level (if enabled)

⸻

## FSM Integration

The FSM accepts this task shape:
```json
{ "type": "signal_scan" }
```

FSM does the following:
	•	Calls generate_signals()
	•	Logs and embeds each result
	•	Triggers memory update or agent injection
	•	Sends high-confidence signals to planner_agent.py

⸻

## NLP Feedback Loop

If a signal fails (e.g. wrong trend), it is:
	1.	Logged to data/logs/bootstrap.log
	2.	Flagged by feedback_loop.py
	3.	Included in generate_dataset.py output
	4.	Used to improve transformer via trainer.py

⸻

## Tax Estimation Logic (US-Only)

If a position is closed in portfolio_tracker.py, then:
	•	tax_estimator.py determines:
	•	Long vs short term
	•	Basis cost vs sale price
	•	Tax category (ordinary, capital gains)
	•	Logs result to memory

Example output:
```json
{
  "symbol": "BBIG",
  "action": "SELL",
  "profit": 52.30,
  "term": "short",
  "taxable": true,
  "timestamp": "2025-05-18T13:30:01Z"
}
```

⸻

## Fault Tolerance
	•	If live scraping fails → defaults to Playwright screener
	•	If API unavailable → uses random simulation from stock_scraper.py
	•	Scraper health checked every 5s via FSM loop

⸻

## Summary

GremlinGPT’s trading_core/ is engineered for:
	•	Momentum trading under $10
	•	Offline-safe signal generation
	•	Vector-tagged pattern detection
	•	Closed-loop learning via failure feedback

Every win teaches the agent reinforcement.

Every failure teaches it mutation.

Every signal becomes a memory.
