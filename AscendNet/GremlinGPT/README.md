# GremlinGPT

**Autonomous. Offline. Self-Evolving.**  
GremlinGPT is a modular AI system designed to bootstrap itself into a local domain-specific LLM through iterative reasoning, mutation, feedback, and retraining — without the cloud.

---

## Table of Contents

- [Overview](#overview)
- [System Features](#system-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Running the System](#running-the-system)
- [System Components](#system-components)
- [Technical Notes](#technical-notes)
- [Recovery & Snapshots](#recovery--snapshots)
- [Troubleshooting](#troubleshooting)
- [Directory Structure](#directory-structure)

---

## Overview

GremlinGPT is a self-hosted recursive agent system with:

- Zero reliance on external APIs
- Full vector memory and attention pipelines
- NLP stack (tokenizer, transformer, parser) built for self-replacement
- DOM scraping + signal analysis tailored for penny stock trading
- A self-training pipeline that mutates failed logic into future embeddings

---

## System Features

- Offline-first PWA dashboard (mobile + desktop)
- FSM-driven agent planning
- Chroma/FAISS memory vector stores
- Prebuilt transformer/embedding core (MiniLM/DistilBERT)
- Dynamic self-training from live logs
- DOM navigator + Playwright simulator
- EMA/VWAP-based penny stock scanner
- UMAP + metadata tagging on all memory

---

## Architecture

All subsystems communicate through a modular, recursive design:

- **Backend** (Flask + SocketIO): Orchestrates commands, routes APIs
- **FSM Agent Core**: Controls tool invocation, retry logic, state snapshots
- **Scraper**: Persistent browser automation, DOM capture, vector storage
- **NLP Engine**: Bootstrap tokenizer/transformer/tagger + mutation diffing
- **Memory**: Vector embeddings stored via Chroma/FAISS with metadata tags
- **Self-Training Loop**: Watches logs, mutates failure data, retrains NLP
- **Frontend Dashboard**: PWA interface for chat, tasks, memory, trading

---

## Installation

1. **Clone the repo**
```bash
git clone https://github.com/statikfintechllc/AscendAI.git && cd ~/AscendAI/AscendNet/GremlinGPT
```
2.	Install Conda envs
cd conda_envs && zsh create_envs.sh

3.	Bootstrap NLP Models (one time)
conda activate gremlin-nlp
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

---

## Running the System
cd run
zsh start_all.sh

This will:
	•	Start the backend server
	•	Launch FSM agent loop
	•	Activate scraping + DOM watcher
	•	Begin feedback-based self-training

Access the dashboard at:
http://localhost:5050/

---

## System Components

1. backend/
	•	Flask API router
	•	NLP/chat routing
	•	Task + memory planners
	•	State snapshots + runtime logs

2. agent_core/
	•	Task queue w/ retry
	•	Tool dispatcher (scrape, scan, train, nlp)
	•	FSM planner + heuristics

3. nlp_engine/
	•	Tokenizer (bert-base-uncased)
	•	Transformer (DistilBERT / MiniLM)
	•	POS, parsing, semantic scoring
	•	Mutation diff engine

4. memory/
	•	FAISS + Chroma vector backends
	•	Metadata + tagging
	•	Embedding IO + indexing

5. scraper/
	•	Playwright DOM sim
	•	BeautifulSoup/LXML navigator
	•	Persistence: cookies + Chromium profiles

6. self_training/
	•	Log triggers via Watchdog
	•	Mutation + feedback ingestion
	•	NLP vector retrainer

7. trading_core/
	•	Penny stock premarket scanner
	•	EMA/VWAP breakout rules
	•	Tax + portfolio model

8. frontend/
	•	PWA dashboard (offline support)
	•	Components: Chat, TaskTree, Memory, Signals
	•	Real-time REST + WebSocket integration

---

## Recovery & Snapshots

GremlinGPT saves state to:
run/checkpoints/state_snapshot.json

To restart from a crash:
zsh reboot_recover.sh

This reloads:
	•	FSM state
	•	Task queue
	•	Memory vector delta
	•	Agent profile settings

---

## Troubleshooting

Port conflict?
Make sure port 5050 is free.

Scraper fails silently?
Check browser profile or run with headless=False.

No embeddings show?
Confirm vector backend is faiss or chromadb and embedder.py is being called.

Self-training not firing?
Ensure watch_logs() is running or manually call trainer.py.

---

## Directory Structure

See docs/full_structure_tree.txt or run:

python run/module_tracer.py

To trace module imports.

---

## Final Notes

This system is not built to “chat”.
It is built to think, evolve, and eventually outgrow its creators.

You are the signal.
Unseen. Unbroken. Unrivaled. Gremlins Ascend.
Welcome to the Gremlin Epoch by AscendAI & statikfintechllc