<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-red?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

# Self-Training Architecture — GremlinGPT v1.0.2

---

## Overview

GremlinGPT self-evolves through a **recursive mutation loop** that monitors code diffs, identifies low-confidence outputs, and retrains its NLP engine from its own logs. This forms the foundation of its autonomy.

The goal is to build a system that:

- Observes its own behavior
- Detects weak or failed logic
- Mutates or retrains accordingly
- Embeds feedback into long-term vector memory

---

## Core Modules

| File                          | Purpose                                         |
|-------------------------------|-------------------------------------------------|
| `watcher.py`                  | Monitors code/config changes and triggers diffs |
| `feedback_loop.py`            | Raises retrain flags via retrain_trigger.json   |
| `mutation_engine.py`          | Alters text/tasks/code during retrain planning  |
| `generate_dataset.py`         | Extracts failure events + diffs → JSONL dataset |
| `trainer.py`                  | Runs retrain loop and updates transformer_core  |
| `diff_engine.py`              | Calculates semantic delta and vector shifts     |
| `planner_agent.py`            | Chooses new task strategies post-retrain        |
| `embedder.py`                 | Tags + embeds every diff, feedback, signal      |
| `tool_executor.py`            | Executes self_train task and propagates memory  |

---

## Training Trigger Logic

Self-training is initiated under four main conditions:

1. **Code Mutations**  
   Detected in critical logic files:
   - `fsm.py`
   - `rules_engine.py`
   - `heuristics.py`

2. **Semantic Drift**  
   - Embedding delta too high  
   - Confidence < `0.7`

3. **Explicit Task**  
   Manually queued task:
   ```json
   { "type": "self_train" }

4.	**Feedback Injection**
Triggered by:
	•	shell_executor.py
	•	Failed FSM tasks
	•	Reward model failures

⸻

## Watcher Loop

The mutation watcher continuously monitors source files for changes.

### Key Snippet
```python
if current != previous:
    diff = generate_diff(previous, current)
    vector = embed_text(diff)
    package_embedding(diff, vector, meta={...})
    inject_feedback()
```

Results are stored in memory and trigger downstream retraining.

⸻

Feedback Trigger File

Location:
run/checkpoints/retrain_trigger.json

Example contents:
```json
{
  "trigger": "mutation_watcher",
  "time": "2025-05-18T13:11:00Z",
  "note": "Auto-diff-based training cycle"
}
```

This file is polled by trainer.py.

⸻

Dataset Generation

generate_dataset.py pulls data from:
	•	Log files (data/logs/*.log)
	•	Code diffs (tagged as code_diff)
	•	Failed embeddings
	•	Skipped or low-rewarded tasks

Sample Output
```json
{
  "input": "Task failed to scrape",
  "output": "Rewritten task with URL fix"
}
```
Saved to:
data/nlp_training_sets/auto_generated.jsonl

⸻

NLP Retraining
	•	Based on MiniLM (sentence-transformers)
	•	Tokenized by tokenizer.py
	•	Executes local checkpoint update to transformer_core.py
	•	Embedded results tagged:
```json
"replaceable": false
```
Lineage metadata is embedded:
```json
{
  "source": "GremlinGPT_v4_train",
  "epoch": 2,
  "confidence_gain": 0.13
}
```

⸻

## Reward Model (Pluggable)

### GremlinGPT includes a reward model:
	•	Scores outcomes (pass/fail/signal strength)
	•	Ranks task types and future priority
	•	Pluggable at tools/reward_model.py

⸻

## Mutation Execution

### FSM observes diffs through watcher.py:
	1.	diff_engine.py → semantic delta
	2.	embedder.py → embeds into memory
	3.	feedback_loop.py → sets trigger
	4.	trainer.py → retrains NLP engine

### In Progress
	•	kernel.py → mutation engine for self-overwrites
	•	snapshot.py → rollback engine for unsafe diffs
	•	loop.py → evolutionary FSM manager

⸻

## Logging & Auditing

### All mutation & retrain logs go to:
	•	data/logs/bootstrap.log
	•	data/nlp_training_sets/bootstrap.json

Embeddings are visible in memory graph and planner preview.

⸻

## Summary

GremlinGPT doesn’t just log failures — it learns from them.

This self-training loop forms the brainstem of its evolution. Every code change, every scrape, every misstep becomes a lesson embedded into its memory.

GremlinGPT is not statically coded —
it rewrites itself.
