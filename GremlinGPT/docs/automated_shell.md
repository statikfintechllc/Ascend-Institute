<div align="center">

  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=white" alt="Fair Use License"/>
  </a>
  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-red?style=for-the-badge&logo=dragon&logoColor=white" alt="GremlinGPT License"/>
  </a>
  
</div>

⸻

# GremlinGPT Autonomous Shell Flow — v1.0.2

GremlinGPT operates a self-mutating, autonomously routed shell loop with embedded vector memory, semantic safety, and live planner feedback—beginning from a single kernel call.

⸻

## Boot Sequence Overview

### Primary Loop Path
	1.	core/loop.py starts:
	•	FSM loop (fsm.py)
	•	Mutation Daemon (mutation_daemon.py)
	•	Dataset generation
	2.	fsm.py:
	•	Dequeues tasks from memory
	•	Executes or escalates based on confidence or error rates
	3.	tool_executor.py:
	•	Executes tools like:
	•	nlp
	•	signal_scan
	•	scrape_live
	•	shell
	•	Calls shell_executor.py for raw commands
	•	Embeds results with embedder.py
	•	Logs events to log_history.py
	4.	reward_model.py:
	•	Scores result quality
	•	Drives planner incentives
	5.	planner_agent.py:
	•	Reviews recent reward memory
	•	Enqueues next task autonomously using vector similarity
	•	Embeds task rationale and injects watermark
	6.	If a file is changed or mutated:
	•	watcher.py detects code deltas
	•	diff_engine.py computes AST + semantic diff
	•	embedder.py packages delta into memory
	•	feedback_loop.py triggers retraining + watermark
	7.	If confidence drops:
	•	mutation_daemon.py may rollback low-semantic mutations
	•	trainer.py retrains model with mutation lineage
	8.	The system cycles forward based on memory, embeddings, reward, and watermark lineage.

⸻

## Autonomous Mutation Safety

### GremlinGPT only accepts mutations that meet all criteria:
Check
Rule
Syntax
Verified with ast.parse()
Semantic Safety
Must pass 0.60 threshold (cosine similarity)
Patch Test
Executes code snippet with run_patch_test()
Watermarking
All patches logged with traceable watermark
Snapshot
Rolled back if semantic degradation detected

Snapshots are versioned in:
run/checkpoints/snapshots/

⸻

## Mutation Path (Kernel)

### When planner chooses to patch code:
	1.	planner_agent.py invokes kernel.py
	2.	kernel.py:
	•	Validates mutation syntax
	•	Backs up original via snapshot.py
	•	Writes mutation to file
	•	Computes semantic + vector delta
	•	Calls package_embedding() and stores patch lineage
	•	Injects watermark
	3.	Triggers training via feedback_loop.py

⸻

## Scraper Integration (Live + DOM)

### GremlinGPT supports dynamic data ingestion via:
Source
Module
TWS or STT running
psutil_check()
Browser scraping
playwright_handler.py
DOM memory mapping
dom_navigator.py
Storage
store_stock_snapshot() embeds each asset vector
Signal scan
signal_generator.py applies vector reward rules
Live data auto-refreshes every 5 seconds.

⸻

## Memory & Watermarking

### All embeddings pass through:
	•	embed_text(): vectorize NLP/code/state
	•	package_embedding(): persist with metadata
	•	inject_watermark(): tag memory lineage

### Watermarks ensure:
	•	Memory traceability
	•	Autonomous lineage validation
	•	Mutation accountability

⸻

## Execution Environment Map

Component
Role
gremlin-orchestrator
FSM loop, kernel patcher
gremlin-nlp
Transformers, scoring, NER
gremlin-memory
Vector storage, retrieval
gremlin-scraper
DOM ingestion, live stock streams
gremlin-dashboard
Full-stack UI + REST interface

⸻

### Startup Flow

```bash
conda activate gremlin-orchestrator && \
python3 core/loop.py
```
### Reboot from Last Known State

```bash
reboot_recover.sh
```

⸻

## Core Logs + Datasets

Purpose
File
Execution Events
data/logs/history/gremlin_exec_log.jsonl
Reward Scores
data/logs/rewards.jsonl
Mutation Embeds
data/nlp_training_sets/live_mutations.jsonl
Portfolio
data/portfolio.json, trade_history.jsonl
Snapshot Metadata
run/checkpoints/snapshots/
Runtime
run/logs/runtime.log

