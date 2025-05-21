# Trading Signals — GremlinGPT v4

---

## Overview

The `trading_core/` subsystem is a modular, offline engine focused on **penny stock discovery, analysis, and signal generation**. It runs autonomously, feeds into vector memory, and influences agent planning via feedback loop retraining.

The goal is to create **precise, actionable market signals** under $10 USD per share with embedded context and confidence scores.

---

## Modules

| File                     | Description                              |
|--------------------------|------------------------------------------|
| `signal_generator.py`    | Detects trading signals using rules      |
| `stock_scraper.py`       | Scrapes premarket & intraday prices      |
| `rules_engine.py`        | Evaluates price trends & patterns        |
| `portfolio_tracker.py`   | Tracks open/closed positions in memory   |
| `tax_estimator.py`       | Computes estimated capital gains (US)    |

---

## Pipeline Flow

stock_scraper] → [rules_engine] → [signal_generator] → [memory/embedder]
---

## Signal Detection Logic

Signals are generated based on:

- **Price Threshold**: Only stocks < $10 USD
- **Pattern Recognition**:
  - EMA crossover (5/20)
  - VWAP gap ups
  - Pre-market momentum
- **Volume Spike Detection**
- **Sentiment correlation** (via NLP from scrape memory)

Each signal produces a JSON like:

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

⸻

## Embedding Signals into Memory

Once generated, signals are passed through:
	1.	semantic_score.py → Vectorization
	2.	package_embedding() → Embedding + tagging
	3.	memory_vector_store/ → FAISS/Chroma backend

Signals are tagged as:
```json
{
  "type": "signal",
  "strategy": "EMA_crossover",
  "source": "trading_core",
  "agent_id": "planner001"
}
```
These become retrievable in:
	•	Dashboard MemoryGraph
	•	Agent planner for downstream task chaining
	•	NLP training set generator

⸻

## Real-Time Refresh

The frontend TradingPanel.js polls signals:
	•	Every 0.2s (configurable)
	•	Uses WebSocket from backend
	•	Auto-refreshes visible stock data

⸻

## Integration with FSM

The FSM (fsm.py) supports task types like:
```json
{ "type": "signal_scan" }
```
	•	This task calls generate_signals() directly
	•	Outputs are stored and passed into planner or shell agents
	•	Confidence scores above threshold may trigger shell alerts or memory embeddings

⸻

## Feedback into NLP Loop

Low-confidence or failed signals:
	•	Are logged to data/logs/bootstrap.log
	•	Passed into mutation_engine.py for refinement
	•	Influence retrain cycles via feedback_loop.py

⸻

## Tax Estimation (US-Only)

When a trade is closed:
	•	portfolio_tracker.py logs entry/exit
	•	tax_estimator.py estimates:
	•	Short-term/long-term status
	•	Taxable event classification
	•	Basis and net PnL

⸻

## Conclusion

GremlinGPT’s trading subsystem is tuned for:
	•	Low-cap, fast-moving stocks
	•	Technical breakout detection
	•	Offline, high-speed signal logic

Every signal becomes a learning opportunity — whether it wins or fails.
