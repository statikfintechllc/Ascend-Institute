# FSM Architecture

The Finite State Machine (FSM) in `agent_core/fsm.py` is the task engine.

### FSM Lifecycle

1. Fetch task from queue (`task_queue.fetch_task`)
2. Evaluate task with `heuristics.py`
3. Execute with `tool_executor.py`
4. On success:
   - Save result
   - Embed if relevant
5. On failure:
   - Retry up to limit
   - Log error in `error_log.py`

### Retry Strategy

- Max retries: `task_retry_limit` from `config.toml`
- Tasks marked `retry` are re-enqueued
- After failure threshold: logged + discarded

### Tool Chain

FSM executes:
- `scrape` → via `playwright_handler`
- `nlp` → via `transformer_core.encode()`
- `signal_scan` → via `generate_signals()`
- `self_train` → via `feedback_loop.inject_feedback()`
