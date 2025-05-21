# GremlinGPT: System Overview

**Version**: 4.0  
**Type**: Autonomous, Offline, Self-Evolving AI  
**Host**: Linux Ubuntu (zsh-compatible)  
**Execution**: Conda-based, multi-GPU optional  
**Interface**: Mobile-first PWA + REST/SocketIO backend

---

## Core Mission

GremlinGPT is a locally hosted recursive intelligence system that:

- Scrapes data, learns from results, and evolves without human oversight
- Operates fully offline with no cloud dependencies
- Grows its own NLP engine using feedback and self-repair
- Can plan, refactor, and upgrade its own code autonomously

---

## Modules and Responsibilities

### 1. `frontend/` (PWA Interface)
- Chat with FSM-driven agents
- Display agent task tree and memory vectors
- Monitor stock signals in real time
- Fully offline-capable via Service Worker

### 2. `backend/`
- Flask + SocketIO API server
- Routes requests to planner, memory, scraper, FSM, etc.
- Interfaces with `planner_agent.py` and `fsm.py`
- Can be tunneled externally via `ngrok_launcher.py`

### 3. `agent_core/`
- Finite State Machine (`fsm.py`) to drive task evaluation
- `task_queue.py` for persistent queueing
- `tool_executor.py` to dispatch actions to NLP, trading, scraping, shell, etc.

### 4. `nlp_engine/`
- Bootstrapped transformer models and tokenizer
- Custom diff engine to analyze mutations
- POS tagging and semantic scoring via SBERT
- All NLP outputs are tagged with:
```json
{
  "source": "bootstrap-prebuilt",
  "model": "MiniLM",
  "replaceable": true
}
```

### 5. `memory/`
	•	Local vector store using FAISS/Chroma
	•	Embedding packaging + tagging
	•	Auto-indexing of scrapes, outputs, plans, deltas
	•	Snapshot and rollback infrastructure included

### 6. `self_training/`
	•	Monitors diffs in core logic (FSM, rules, agents)
	•	Generates embedding deltas + diff logs
	•	Injects feedback into retrain queue
	•	Triggers NLP mutation and log-based dataset generation

### 7. `trading_core/`
	•	Scans for penny stocks under $10
	•	Uses EMA/VWAP for intraday pattern recognition
	•	Generates signals and embeds them into memory
	•	Signals feed into reward scoring and planner

### 8. `scraper/`
	•	Browser automation via Playwright
	•	DOM graph navigation and page capture
	•	Stores structured HTML + snapshots
	•	Tied directly to memory for analysis

### 9. `planner_agent.py`
	•	Uses graph state + logs + vector space to plan next actions
	•	Reads task history, memory tags, and results
	•	Enqueues task trees for FSM execution

### 10. `agent_shell/`
	•	Executes secure Linux commands via subprocess
	•	Wraps results in structured memory packages
	•	Callable from planner tasks (e.g. {"type": "shell", "command": "df -h"})

⸻

## Execution Model
	•	start_all.sh spins up all environments and FSM loop
	•	ngrok_launcher.py runs automatically if enabled in config.toml
	•	watcher.py diff-scans key modules and stores changes in memory
	•	feedback_loop.py links code changes → NLP retraining
	•	fsm.py continuously pulls from queue and dispatches tools
	•	planner_agent.py injects tasks based on logs and signal memory

⸻

## System Resilience
	•	reboot_recover.sh restores last snapshot and memory index
	•	All embeddings, task trees, and logs are serialized to disk
	•	Git-style rollback support built into core/snapshot.py
	•	Each mutation, reward, or crash is logged with diff + score

⸻

## Key Technologies
	•	Python 3.10 (Conda-managed)
	•	Flask + SocketIO + Dash + Plotly
	•	FAISS + Chroma for vector search
	•	HuggingFace Transformers, SentenceTransformer, spaCy, nltk
	•	Playwright, BeautifulSoup, LXML
	•	PyYAML, Click, Watchdog, NetworkX, Loguru

⸻

## Runtime Requirements
	•	Linux Ubuntu (tested), zsh or bash shell
	•	~8GB RAM min, GPU acceleration optional
	•	3+ conda environments:
	•	gremlin-nlp, gremlin-dashboard, gremlin-orchestrator, etc.

⸻

## Accessing the Dashboard on Mobile
	1.	Ensure ngrok is enabled in config.toml
	2.	Run start_all.sh
	3.	Copy printed public URL (e.g. https://abc123.ngrok.io)
	4.	Open on your phone and “Add to Home Screen” (PWA)
	5.	You now have full control of GremlinGPT on mobile

⸻

## Conclusion

GremlinGPT v4 is not just an AI agent — it is an autonomous, evolving intelligence capable of:
	•	Self-directed growth
	•	Self-repair
	•	Embedded mutation and recovery
	•	Modular upgrades
	•	Zero external dependencies

Built not to run a prompt — but to rewrite itself.
