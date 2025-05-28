<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>
	
<h1 align= "center">GremlinGPT: The real Autonomous Agent v1.0.3</h1>

<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/GremlinGPT">
    <img src="https://img.shields.io/badge/build-v1.0.2-darkred?labelColor=black" alt="Build Status"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About%20Us/FOUNDER_LOG.md">
    <img src="https://img.shields.io/badge/Founder's%20Log-Manifesto-darkred?labelColor=black" alt="Founder's Log"/>
  </a>
  <br/>
  <a href="https://github.com/statikfintechllc">
    <img src="https://img.shields.io/badge/contributors-2-darkred?labelColor=black" alt="Contributors"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About%20Us/FOUNDER_STATEMENT.md">
    <img src="https://img.shields.io/badge/Founder's%20Log-Statement-darkred?labelColor=black" alt="Founder's Log"/>
  </a>
</div>

---

<h1 align="center">AscendAI Traffic</h1>
<h1 align="center">
  <a href="https://raw.githubusercontent.com/statikfintechllc/AscendAI/main/docs/traffic_graph.png">
  <img src="https://raw.githubusercontent.com/statikfintechllc/AscendAI/main/docs/traffic_graph.png" alt="Traffic Graph" />
  </a>
</div>
  
<h1 align="center">**Reset: 10:00pm CST**</h1>

---

## Table of Contents

- [Founder's Log & Manifesto](#founders-log--manifesto)
- [Overview](#overview)
- [System Features](#system-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Running the System](#running-the-system)
- [System Components](#system-components)
- [Recovery & Snapshots](#recovery--snapshots)
- [Troubleshooting](#troubleshooting)
- [System Infrastructure](#system-infrastructure)

⸻

## Founder's Log & Manifesto

> I built an AI system that builds itself.  
> Not in a lab.  
> Not at a venture-backed startup.  
> Not on fiber internet with a dev team holding my hand...

Curious about the journey, the pain, and the philosophy behind AscendAI?  
Read more in the [FOUNDER_LOG.md](https://github.com/statikfintechllc/AscendAI/blob/master/About%20Us/FOUNDER_LOG.md)

⸻

## Overview

GremlinGPT is a self-hosted recursive agent system with:

- Zero reliance on external APIs
- Full vector memory and attention pipelines
- NLP stack (tokenizer, transformer, parser) built for self-replacement
- DOM scraping + signal analysis tailored for penny stock trading
- A self-training pipeline that mutates failed logic into future embeddings

⸻

## System Features

- Offline-first PWA dashboard (mobile + desktop)
- FSM-driven agent planning
- Chroma/FAISS memory vector stores
- Prebuilt transformer/embedding core (MiniLM/DistilBERT)
- Dynamic self-training from live logs
- DOM navigator + Playwright simulator
- EMA/VWAP-based penny stock scanner
- UMAP + metadata tagging on all memory

⸻

### 🔬 Mutation Zone Activated

The `dev-experiment/` sandbox is now scaffolded and online.

- 🧠 `memory_hacking/` → custom embeddings, reward injection
- 🤖 `new_agents/` → speculative planners, FSM mutators, self-reflection nodes
- 🔥 `broken_scrapers/` → crash rigs, instability injectors
- 📜 `your_mutations_here.md` → invitation to mutate the system directly

> Fork. Inject. Break. Log.  
> The Gremlin remembers every mutation.

⸻

## Architecture

All subsystems communicate through a modular, recursive design:

- **Backend** (Flask + SocketIO): Orchestrates commands, routes APIs
- **FSM Agent Core**: Controls tool invocation, retry logic, state snapshots
- **Scraper**: Persistent browser automation, DOM capture, vector storage
- **NLP Engine**: Bootstrap tokenizer/transformer/tagger + mutation diffing
- **Memory**: Vector embeddings stored via Chroma/FAISS with metadata tags
- **Self-Training Loop**: Watches logs, mutates failure data, retrains NLP
- **Frontend Dashboard**: PWA interface for chat, tasks, memory, trading

⸻

## Installation

1. **Clone the repo**
```bash
git clone https://github.com/statikfintechllc/AscendAI.git && cd ~/AscendAI/AscendNet/GremlinGPT
```

2.	Bootstrap NLP Models (one time)
```bash
conda activate gremlin-nlp && \
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')" && \
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

3.	Install and Build Conda envs
```bash
cd ~/AscendAI/GremlinGPT/conda_envs && sudo chmod +x create_envs.sh && ./create_envs.sh
```

or

```bash
cd ~/AscendAI/GremlinGPT && sudo chmod +x install.sh && ./install.sh
```

⸻

## Running the System
```bash
cd run && sudo chmod +x start_all.sh && ./start_all.sh
```

What happens:
	•	Backend server goes live
	•	FSM starts looping
	•	Browser scraper engages
	•	Feedback engine boots

Access dashboard at:
http://localhost:5050/

⸻

## System Components

1. backend/
	•	Flask API router
	•	NLP/chat routing
	•	Task + memory planners
	•	State snapshots + runtime logs

2. agent_core/
	•	Task queue w/ retry
	•	Tool dispatcher (scrape, scan, train, nlp, shell executor)
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

⸻

## Recovery & Snapshots

GremlinGPT auto-saves:
	•	Agent state
	•	Task queue
	•	Memory deltas
 
GremlinGPT saves state to:
~/AscendAI/GremlinGPt/run/checkpoints/state_snapshot.json

For Viewing:
```bash
cat ~/AscendAI/GremlinGPT/run/checkpoints/state_snapshot.json
```

To test pre-launch:
```bash
cd ~/AscendAI/GremlinGPT && sudo chmod +x test_system_start.sh && ./test_system_start.sh
```

To monitor:
```bash
tail -f run/logs/runtime.log
```

To resume from crash:
```bash
cd ~/AscendAI/GremlinGPT && sudo chmod +x reboot_recover.sh && ./reboot_recover.sh
```

This reloads:
	•	FSM state
	•	Task queue
	•	Memory vector delta
	•	Agent profile 
 
⸻

Troubleshooting
	•	Port 5050 busy? Kill or remap in config.
	•	Scraper fails silently? Set headless=False in playwright_handler.py
	•	No memory? Recheck embedder.py and Chroma/FAISS path.
	•	Training loop inactive? Trigger trainer.py manually or inspect Watchdog.

⸻

## System Infrastructure

**This is not just architecture — it’s the nervous system of an evolving intelligence.**  
Blueprints, memory pipelines, call graphs, and recovery rituals all live here:

`~/AscendAI/GremlinGPT/docs/`

Explore:
- `full_structure_tree.txt` — full module hierarchy, no secrets
- `system_overview.md` — how the mind is wired
- `system_call_graph.md` — what talks to what, and why
- `fsm_architecture.md` — the agent loop’s recursive core
- `memory_pipeline.md` — vector thought, storage, and recall
- `trading_signals.md` — the pattern seer for penny chaos
- `self_training.md` — how failure becomes fuel
- `ngrok_integration.md` — remote infiltration hooks
- `gremlin.service.md` — daemonize the beast
- `automated_shell.md` — command-line possession

To trace the system live, run:
```bash
python run/module_tracer.py
```

⸻
