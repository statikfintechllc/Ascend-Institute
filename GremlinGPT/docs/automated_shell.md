# GremlinGPT Autonomous Shell Flow

GremlinGPT runs a **self-sustaining shell loop**, starting from a single kernel call.

---

## Boot Flow

1. `core/loop.py` launches persistent FSM + retrain trigger check
2. `fsm.py` dequeues tasks from memory
3. `tool_executor.py` calls tools or dispatches `python_executor.py`
	•	tool_executor.py also supports "shell" task type for executing commands via shell_executor.py
	•	Output is logged, scored, and embedded
4. Task results are scored by `reward_model.py`
5. Execution logs are stored in `log_history.py`
6. If diffs or failures are detected:
   - `watcher.py` logs diff
   - `embedder.py` packages it
   - `feedback_loop.py` triggers retrain
7. `planner_agent.py` reviews memory + reward history and queues the next task
7.5. If no tasks are queued, planner_agent.py generates next task using reward memory and NLP vector similarity.
8. The cycle repeats

---

## Mutation Safety Protocol

To prevent logic degradation:
- Mutated code is verified for syntax (`ast.parse`)
- Semantic similarity must exceed 0.6
- If unsafe, original code is restored
- Snapshots are stored in `run/checkpoints/snapshots/`

---

## Kernel Mutation Path

When a rewrite is planned:

- `kernel.py` is invoked by planner or dashboard
- Applies code patch to target module
- Calls `snapshot.py` to embed and version the old file
- All changes are embedded and logged
- Triggers mutation retrain from `feedback_loop.py`

---

## Execution Environment

| Environment        | Role                           |
|--------------------|--------------------------------|
| gremlin-orchestrator | Loop, planner, kernel         |
| gremlin-nlp        | Embedding + scoring             |
| gremlin-memory     | Storage + vector store          |
| gremlin-scraper    | Playwright & DOM tools          |
| gremlin-dashboard  | Frontend + backend UI/API       |

---

## Start the Shell

```bash
conda activate gremlin-orchestrator && \
python3 core/loop.py
```

Restart From Snapshot
```bash
reboot_recover.sh
```

⸻

Logs Stored
	•	data/logs/history/gremlin_exec_log.jsonl
	•	data/logs/rewards.jsonl
	•	run/logs/runtime.log
