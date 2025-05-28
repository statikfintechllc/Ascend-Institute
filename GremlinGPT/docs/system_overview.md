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

# GremlinGPT: System Overview

**Version**: 1.0.3
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

1. `frontend/` (PWA Interface)
- Chat with FSM-driven agents  
- Display agent task tree and memory vectors  
- Monitor stock signals in real time  
- Fully offline-capable via Service Worker  

2. `backend/`
- Flask + SocketIO API server  
- Routes requests to planner, memory, scraper, FSM, etc.  
- Interfaces with `planner_agent.py` and `fsm.py`  
- Can be tunneled externally via `ngrok_launcher.py`  

3. `agent_core/`
- `fsm.py`: Finite State Machine to drive task logic  
- `task_queue.py`: Persistent queueing and retry handling  
- `tool_executor.py`: Dispatches tool tasks (scraper, NLP, trading, shell, etc.)  
- `heuristics.py`: Conditions for task execution  

4. `nlp_engine/`
- Bootstrapped transformer models and tokenizer  
- Custom diff engine to analyze mutations  
- POS tagging, semantic scoring (SBERT, MiniLM)  
- All outputs tagged like:
```json
{
  "source": "bootstrap-prebuilt",
  "model": "MiniLM",
  "replaceable": true
}
```
5. memory/
	•	Local vector store using FAISS/Chroma
	•	embedder.py: Handles vectorization and metadata
	•	Auto-indexes scrapes, signals, code diffs, and planner outputs
	•	snapshot.py: Periodic memory snapshots for recovery

6. self_training/
	•	watcher.py: Tracks file changes
	•	diff_engine.py: Measures semantic drift
	•	generate_dataset.py: Builds training sets
	•	feedback_loop.py: Raises retrain triggers
	•	trainer.py: Executes NLP retrain locally

7. trading_core/
	•	Scans for penny stocks under $10
	•	Uses VWAP/EMA logic to find momentum setups
	•	signal_generator.py pushes structured alerts
	•	Signals are embedded and fed to the reward model

8. scraper/
	•	Automated scraping with Playwright
	•	Extracts DOM graph and page summaries
	•	Uses page_simulator.py + dom_navigator.py for HTML analysis
	•	Outputs embedded vectors for memory and training

9. planner_agent.py
	•	Builds new task trees based on:
	•	Prior reward scores
	•	Memory similarity
	•	Current execution context
	•	Injects tasks to FSM automatically

10. agent_shell/
	•	shell_executor.py: Runs safe subprocess commands
	•	Stores structured output with memory trace
	•	Can be triggered by planner (e.g. "type": "shell")

⸻

## Execution Model
	•	start_all.sh: Boots entire system
	•	ngrok_launcher.py: Opens external tunnel if enabled
	•	fsm.py: Core autonomous loop
	•	planner_agent.py: Injects tasks from memory and logs
	•	watcher.py: Monitors mutation
	•	feedback_loop.py: Retrains NLP engine via vector deltas
	•	tool_executor.py: Runs NLP/Signal/Scrape/Shell pipelines

⸻

## System Resilience
	•	reboot_recover.sh: Restores last memory snapshot
	•	core/snapshot.py: Stores vectorized diffs and state checkpoints
	•	Git-like rollback for broken FSM/logic mutations
	•	Each reward, crash, or code change is archived with traceability

⸻

## Key Technologies
	•	Language: Python 3.10
	•	Frontend: React + SocketIO + Dash + PWA
	•	Vector Search: FAISS (default) or Chroma
	•	NLP: SentenceTransformers (MiniLM), HuggingFace, spaCy
	•	Scraping: Playwright, BeautifulSoup, LXML
	•	Monitoring: psutil, Watchdog, Loguru
	•	Persistence: SQLite, JSONL, Checkpoint Snapshots

⸻

## Runtime Requirements
	•	Linux (tested: Ubuntu 22.04+)
	•	zsh or bash shell
	•	~8GB RAM minimum
	•	Optional GPU (CUDA/ROCm)
	•	Conda environments:
	•	gremlin-nlp
	•	gremlin-orchestrator
	•	gremlin-dashboard

⸻

Mobile Dashboard Access
	1.	Set [ngrok.enabled] = true in config.toml
	2.	Run:
```bash
bash run/start_all.sh
```
3.	Scan printed ngrok URL or open it on phone
	4.	Install PWA by “Add to Home Screen”
	5.	GremlinGPT is now mobile-ready and remotely accessible

⸻

## Conclusion

GremlinGPT v1.0.2 is not a chatbot.
It is an autonomous intelligence kernel that:
	•	Rewrites its logic
	•	Learns from errors
	•	Recovers from failures
	•	Evolves toward better reasoning

Built not to simply respond to a prompt —
but to write the next one itself.
