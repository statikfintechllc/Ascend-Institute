# Self-Training Architecture — GremlinGPT v4

---

## Overview

GremlinGPT self-evolves through a **recursive mutation loop** that monitors code diffs, identifies low-confidence outputs, and retrains its NLP engine from its own logs. This forms the foundation of its autonomy.

The goal is to create a system that:
- Observes its own behavior
- Identifies weak or failed logic
- Mutates or retrains accordingly
- Embeds results into memory for future tasks

---

## Core Modules

| File                           | Purpose                                      |
|--------------------------------|----------------------------------------------|
| `watcher.py`                   | Monitors for code or config mutations        |
| `feedback_loop.py`            | Triggers retrain cycles                      |
| `mutation_engine.py`          | Plans changes based on logs/diffs            |
| `generate_dataset.py`         | Builds new fine-tune dataset from memory     |
| `trainer.py`                  | Executes the local NLP retraining loop       |
| `diff_engine.py`              | Compares embeddings and source deltas        |
| `planner_agent.py`            | Responds to retrained signals with new task strategies |
| `embedder.py`                 | Tags and embeds diff/feedback data           |
| `tool_executor.py`            | Executes retraining triggers and sends feedback loops |

---

## Training Trigger Logic

Training cycles are triggered by:

1. Code changes to:
   - `fsm.py`
   - `rules_engine.py`
   - `heuristics.py`

2. Semantic failure detection:
   - Vector delta too high
   - Confidence below 0.7

3. Manual task like:
```json
{ "type": "self_train" }
```
4.	Mutation feedback from:
	•	agent_shell/shell_executor.py
	•	FSM log deltas
	•	Reward failure

⸻

## Watcher Loop

The mutation watcher scans source code for change every cycle.

### Key Logic
```python
if current != previous:
    diff = generate_diff(previous, current)
    vector = embed_text(diff)
    package_embedding(diff, vector, meta={...})
    inject_feedback()
```
This stores every code mutation as a vector in memory, with metadata.

⸻

## Feedback Injection

Trigger file:
run/checkpoints/retrain_trigger.json

Contents:
```json
{
  "trigger": "mutation_watcher",
  "time": "2025-05-18T13:11:00Z",
  "note": "Auto-diff-based training cycle"
}
```

Checked periodically by trainer.py.

⸻

## Dataset Generation

generate_dataset.py pulls from:
	•	data/logs/*.log
	•	vector memory (tag: code_diff, failure_event)
	•	low-scoring signals or planner results

Outputs a JSONL file for retraining.

Example entry:
```json
{ "input": "Task failed to scrape", "output": "Rewritten task with URL fix" }
```

⸻

NLP Retraining
	•	Uses SentenceTransformer backbone (MiniLM)
	•	Tokenized using tokenizer.py
	•	Retrains are local only
	•	Updates transformer_core.py checkpoint
	•	Tagged output: "replaceable": false

Once a model is upgraded, its lineage is tracked via:
```json
{
  "source": "GremlinGPT_v4_train",
  "epoch": 2,
  "confidence_gain": 0.13
}
```

⸻

## Reward Model (Pluggable)

Gremlin supports a pluggable reward evaluation engine:
	•	Scores success/failure of agent outcomes
	•	Applies reinforcement curve to planner logic
	•	tools/reward_model.py (planned)

⸻

## Mutation Execution

Current FSM watches for changes via watcher.py. When diffs are detected:
- `diff_engine.py` computes semantic deltas
- `embedder.py` embeds diff + metadata
- `feedback_loop.py` raises retrain flag
- `trainer.py` rebuilds the transformer checkpoint

Planned additions:
- `kernel.py` will apply its own rewrites
- `snapshot.py` will rollback unsafe mutations
- `loop.py` will persistently evolve internal logic

⸻

## Logging + Auditing

All self-train cycles log to:

data/logs/bootstrap.log
data/nlp_training_sets/bootstrap.json

Embeddings and mutation lineage are queryable via dashboard and memory API.

⸻

## Conclusion

GremlinGPT doesn’t just log errors — it mutates from them.
This self-training loop is how it rewrites itself, improves its reasoning, and evolves toward autonomy.

Every scrape.
Every signal.
Every failure.
Becomes its next lesson.
