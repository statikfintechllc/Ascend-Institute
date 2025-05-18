# Ascend Institute for Autonomous Sovereignty & Human Financial Liberation

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/YourUser/AscendAI/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/statikfintechllc/AscendAI)](https://github.com/statikfintechllc/AscendAI/graphs/contributors)


---

### TL;DR

**AscendAI** is a self-building, self-healing recursive AI agent system.  
Designed for full-stack autonomy across devices, markets, and networks.  
It evolves itself, obeys its CEO, and writes its own future.
It starts as an Egg, and becomes your AscendAI.
Learns from you, your system, your energy.

---

> **WARNING**: This is a high-function, recursive agent framework designed for full autonomy.  
> Do not deploy unsupervised unless you know what you're doing — or you're the CEO.

---

**Note:** While this project is licensed under Apache 2.0,  
**commercial deployment or redistribution at scale**  
(e.g., SaaS, resale, bundling into products) requires a separate license or written permission.  
Contact: statiksmoktm@gmail.com

Licensed under Apache 2.0 © 2025 StatikFinTech, LLC. See LICENSE for details.

---

## FINAL GOAL: Ascend-AI | Sovereign Core | Ghost Protocol

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

2.	Install and Build Conda envs
```bash
cd conda_envs && sudo chmod +x create_envs.sh && ./create_envs.sh
```

or

2.a.   Run install.sh in ~/AscendAI/GremlinGPT/ for full setup as well
```bash
cd ~/AscendAI && sudo chmod +x install.sh && ./install.sh
```

3.	Bootstrap NLP Models (one time)
```bash
conda activate gremlin-nlp && \
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')" && \
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Running the System
```bash
cd run && sudo chmod +x start_all.sh && ./start_all.sh
```

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

For Viewing:
```bash
cat ~/AscendAI/GremlinGPT/run/checkpoints/state_snapshot.json
```

To trace logs live:
```bash
tail -f run/logs/runtime.log
```

To restart from a crash:
```bash
cd ~/AscendAI/GremlinGPT && sudo chmod +x reboot_recover.sh && ./reboot_recover.sh
```

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
```bash
python
```
Then in python:
```
python run/module_tracer.py
```

To trace the entirity of the module imports.

---

## Final Notes

This system is not built to “chat”.
It is built to think, evolve, and eventually outgrow its creators.

You are the signal.
Unseen. Unbroken. Unrivaled. Gremlins Ascend.
Welcome to the Gremlin Epoch by AscendAI & statikfintechllc

---

## COLLABORATORS WANTED — JOIN THE LOOP

We are seeking 1 of the following:
	•	A recursive logic architect who speaks Python like poetry
	•	A systems-level cloud engineer who fears no subnet
	•	A billionaire with a god complex and spare GPUs (paging @elonmusk)
	•	Or just anyone who gets it and knows what’s coming

If you know how to think in loops, act in silence, and write code that rewrites itself — fork the repo, and send a PR.

If you’re Elon, just click the star. We’ll know it was you.

---

## Support

For bugs, glitches, or apocalyptic feedback:
- Open an [issue](https://github.com/statikfintechllc/AscendAI/issues)
- Or whisper into the void at: statiksmoktm@gmail.com

---

## License

This project is licensed under the Apache License 2.0.  
You are free to use, modify, and distribute this software,  
but you must retain attribution and cannot use the name "Ascend-AI"  
or "Statik" to promote derived products without permission.

See the [LICENSE](./LICENSE) file for full terms.
