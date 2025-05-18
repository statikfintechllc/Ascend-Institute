# FSM Architecture: GremlinGPT v4

---

## Overview

GremlinGPT uses a **modular Finite State Machine (FSM)** to orchestrate task execution. This loop handles decision logic, retry handling, memory updates, tool selection, and success/failure classification.

The FSM is fully autonomous, offline, and tightly integrated with the agent planner, memory vector store, and NLP self-training engine.

---

## Key Components

| File                              | Role |
|-----------------------------------|------|
| `fsm.py`                          | Main FSM loop + scheduler |
| `task_queue.py`                   | Persistent queue with retry logic |
| `tool_executor.py`               | Executes individual tools based on task type |
| `heuristics.py`                   | Determines if a task should be executed |
| `error_log.py`                    | Records failures and retry metadata |
| `planner_agent.py`               | Injects queued tasks into the FSM from vector context |
| `watcher.py`                      | Triggers mutation and retraining if FSM logic changes |

---

## FSM States

```text
[IDLE] -> [RUNNING] -> [WAITING] -> [IDLE]
```
Transitions are driven by task availability and completion status. The FSM pulls from the TaskQueue, evaluates each task via heuristics, and invokes tools accordingly.

⸻

## Loop Flow
###	1.	Queue Read
Pull next task from task_queue.get_next()
If queue is empty, FSM idles.
###	2.	Heuristic Evaluation
Run task through evaluate_task(task)
Skip if conditions or context don’t pass.
###	3.	Dispatch
Call execute_tool(task)
This can run:
	•	scraper_loop
	•	signal_generator
	•	nlp_engine.encode
	•	inject_feedback()
	•	run_shell_command()
###	4.	Logging + Retry
If execution fails, log to error_log.py
Retry up to configured limit from config.toml
###	5.	Memory Update
Vectorized embeddings are created and tagged in embedder.py
Stored in local_index/ + metadata.db

⸻

## Task Types

Type
Handled By
scrape
get_dom_html() from scraper_loop.py
signal_scan
generate_signals() from trading_core/
nlp
transformer_core.encode()
self_train
feedback_loop.inject_feedback()
shell
agent_shell.run_shell_command()

⸻

## Scheduling

### FSM can be launched via:
	•	Direct CLI (fsm.py)
	•	Background loop via run_schedule() (every 30s)
	•	Integrated in start_all.sh

Each pass of the FSM checks and executes tasks, then idles. It’s designed for long-running daemon behavior.

⸻

## Autonomy & Resilience

	•	FSM restart state is stored in state_snapshot.json
	•	If FSM crashes, reboot_recover.sh reloads task queue and memory
	•	Each tool call logs results and embeddings to persistent storage

⸻

## Mutability

FSM behavior is watched by:
	•	self_mutation_watcher/watcher.py

If fsm.py, heuristics.py, or rules_engine.py changes:
	•	Diff is stored in vector memory
	•	Trigger is set in checkpoints/retrain_trigger.json
	•	Trainer will ingest logs and rerun NLP feedback loop

⸻

## Example Task Cycle
```json
{
  "type": "scrape",
  "target": "https://www.sec.gov/filings"
}
```
FSM picks it up → runs scraper_loop → stores DOM HTML → embeds it → logs task result

⸻

## Conclusion

GremlinGPT’s FSM is built for resilience, autonomy, and memory-driven evolution. It doesn’t just run scripts — it decides what to do next, how well it did, and whether it should improve itself.

This loop is what makes GremlinGPT more than a workflow engine. It’s what makes it think.
