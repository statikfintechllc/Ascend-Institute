<div align="center">
  <img src="https://img.shields.io/badge/Fair%20Use-GremlinGPT%20v1.0-black?style=for-the-badge&labelColor=black&color=red&logo=ghost&logoColor=red" alt="GremlinGPT Fair Use">
</div>

# GremlinGPT System Flow (v1.0.2)

## Full Pipeline Graph — Autonomous + NLP-Aware + Mutation-Safe
                                                   ┌────────────────────┐
                     generate_dataset.py           │   ChatInterface.js │
                             ▲                     └────────────────────┘
                             │                             ▲
                        trainer.py                         │
                             ▲                             │
              ┌────────── transformer_core.py ◄────────────┘
              │                  ▲
         pos_tagger.py           │              parse_nlp()
              ▲                  │                    ▲
      tokenizer.py ◄─────────────┴─────┐        semantic_score.py
              ▲                        │                 ▲
          commands.py ◄──── chat_handler.py ──────► embedder.py ◄─────┐
              │                  ▲                  ▲                 │
              │                  │            feedback_loop.py        │
              │                  │                  ▲                 │
              ▼                  ▼                  │                 │
       planner_agent.py ◄────── router.py ◄─────────┘                 │
              │                  ▲                                    │
              │             server.py                                 │
              ▼                                                      │
        task_queue.py ◄───────────── fsm.py ◄─────────────┐          │
              ▲                     │                     │          │
              │                     ▼                     ▼          │
  update_position()         tool_executor.py ───────→ shell_executor.py
              ▲                     │                     ▲          │
  portfolio_tracker.py              │                     │          │
              ▲                     ▼                     │          │
  TradingPanel.js ─────────→ signal_generator.py          │          │
                                  │                       │          │
                                  ▼                       │          │
                         rules_engine.py         log_event + retry  │
                                  ▲                                 │
                    get_live_penny_stocks()                         │
                                  ▲                                 │
                        stock_scraper.py ◄──── scraper_loop.py ◄────┘
                                  ▲                    ▲
                                  │                    │
                    psutil → tws_handler.py     playwright_handler.py
                                  ▲                    ▲
                                  └───── dom_navigator.py ◄──── page_simulator.py

                                          │
                                          ▼
                                  vector_store/memory


⸻

## GremlinGPT Full Script Call Graph (fully extended-beta)

#### GremlinGPT v1.0.2 — Full Script Call Graph

## Nodes

- server.py
- router.py
- scheduler.py
- state_manager.py
- chat_handler.py
- memory_api.py
- scraping_api.py
- planner.py
- commands.py
- fsm.py
- task_queue.py
- tool_executor.py
- heuristics.py
- embedder.py
- tokenizer.py
- transformer_core.py
- semantic_score.py
- diff_engine.py
- feedback_loop.py
- trainer.py
- generate_dataset.py
- mutation_engine.py
- playwright_handler.py
- dom_navigator.py
- page_simulator.py
- scraper_loop.py
- signal_generator.py
- stock_scraper.py
- rules_engine.py
- ChatInterface.js
- MemoryGraph.js
- TaskTreeView.js
- TradingPanel.js
- app.js
- shell_executor.py
- python_executor.py
- portfolio_tracker.py

## Connections

- server.py → router.py
- router.py → chat_handler.py, planner.py, scraping_api.py, memory_api.py
- chat_handler.py → commands.py, tokenizer.py, transformer_core.py, embedder.py
- planner.py → signal_generator.py, task_queue.py
- signal_generator.py → stock_scraper.py, rules_engine.py, embedder.py
- memory_api.py → embedder.py
- scraping_api.py → task_queue.py
- fsm.py → task_queue.py, tool_executor.py, heuristics.py
- tool_executor.py → scraper_loop.py, feedback_loop.py, transformer_core.py, signal_generator.py, shell_executor.py
- shell_executor.py → subprocess, logger, memory
- python_executor.py → subprocess, vector memory
- feedback_loop.py → embedder.py
- trainer.py → feedback_loop.py, mutation_engine.py, generate_dataset.py
- scraper_loop.py → playwright_handler.py, page_simulator.py
- page_simulator.py → dom_navigator.py, embedder.py
- app.js → ChatInterface.js, MemoryGraph.js, TaskTreeView.js, TradingPanel.js
- TradingPanel.js → planner.py
- TaskTreeView.js → fsm.py, embedder.py
- MemoryGraph.js → memory_api.py
- commands.py → embedder.py, parse_nlp(), route inference
- parse_nlp() → tokenizer.py, pos_tagger.py, transformer_core.py
- portfolio_tracker.py → embedder.py, feedback, logger, TradingPanel.js

⸻

## GremlinGPT v1.0.2 – Full Module Call Graph
---
→ backend/server.py

Handles app instantiation and routing.
	•	↳ backend/router.py
	•	↳ backend/api/chat_handler.py
	•	↳ nlp_engine/tokenizer.py
	•	↳ nlp_engine/transformer_core.py
	•	↳ memory/vector_store/embedder.py
	•	↳ backend/api/planner.py
	•	↳ trading_core/signal_generator.py
	•	↳ trading_core/rules_engine.py
	•	↳ trading_core/stock_scraper.py
	•	↳ agent_core/task_queue.py
	•	↳ backend/api/scraping_api.py
	•	↳ agent_core/task_queue.py
	•	↳ backend/api/memory_api.py
	•	↳ memory/vector_store/embedder.py

---

→ agent_core/fsm.py

Main task loop and execution controller.
	•	↳ agent_core/task_queue.py
	•	↳ agent_core/tool_executor.py
	•	↳ scraper/scraper_loop.py
	•	↳ scraper/playwright_handler.py
	•	↳ scraper/page_simulator.py
	•	↳ scraper/dom_navigator.py
	•	↳ memory/vector_store/embedder.py
	•	↳ nlp_engine/transformer_core.py
	•	↳ self_training/feedback_loop.py
	•	↳ trading_core/signal_generator.py
	•	↳ agent_shell/shell_executor.py
	•	↳ agent_core/heuristics.py
	•	↳ self_mutation_watcher/watcher.py
	•	↳ agents/planner_agent.py
	•	↳ memory/vector_store/embedder.py

---

→ core/kernel.py

Code patching + safe mutation handler.
	•	↳ nlp_engine/diff_engine.py
	•	↳ memory/vector_store/embedder.py
	•	↳ self_training/feedback_loop.py
	•	↳ core/snapshot.py

---

→ core/loop.py

Startup & scheduling.
	•	↳ self_training/feedback_loop.py
	•	↳ agent_core/fsm.py

---

→ scraper/scraper_loop.py

HTML & data scraping flow.
	•	↳ scraper/playwright_handler.py
	•	↳ scraper/page_simulator.py
	•	↳ scraper/dom_navigator.py
	•	↳ memory/vector_store/embedder.py

---

→ self_mutation_watcher/mutation_daemon.py

Autonomous mutation observer.
	•	↳ self_mutation_watcher/watcher.py
	•	↳ agents/planner_agent.py
	•	↳ memory/vector_store/embedder.py
	•	↳ nlp_engine/semantic_score.py
	•	↳ agent_core/task_queue.py

---

→ self_training/trainer.py

Watches logs and regenerates training datasets.
	•	↳ watchdog
	•	↳ self_training/generate_dataset.py
	•	↳ self_training/mutation_engine.py
	•	↳ self_training/feedback_loop.py

---

→ self_training/generate_dataset.py

Searches logs/files for anomalies to train on.

---

→ nlp_engine/parser.py

Tokenization, POS tagging, routing, code parsing.
	•	↳ nlp_engine/tokenizer.py
	•	↳ nlp_engine/pos_tagger.py
	•	↳ memory/vector_store/embedder.py

---

→ nlp_engine/transformer_core.py

Encodes sentence embeddings.
	•	↳ transformers.AutoModel
	•	↳ torch.no_grad()

---

→ agent_shell/shell_executor.py

Runs shell commands, captures stdout/stderr.
	•	↳ subprocess.run()
	•	↳ memory/vector_store/embedder.py

---

→ tools/reward_model.py

Scores task outputs based on effectiveness.
	•	↳ nlp_engine/semantic_score.py
	•	↳ memory/vector_store/embedder.py

---

→ frontend/app.js

Main UI framework entrypoint.
	•	↳ ChatInterface.js → /api/chat
	•	↳ TaskTreeView.js → /api/agent/tasks
	•	↳ MemoryGraph.js → /api/memory/graph
	•	↳ TradingPanel.js → /api/trading/signals

---

→ trading_core/portfolio_tracker.py

Manages and logs position history.
	•	↳ memory/vector_store/embedder.py
	•	↳ backend/globals.py

---

→ tests/test_nlp.py, test_scraper.py, etc.

Unit + memory integration tests.

---

# GremlinGPT Full Script Call Graph (fully extended-beta)

## GremlinGPT/agent_core/error_log.py

**Calls:**

- `logger.error`


## GremlinGPT/agent_core/fsm.py

**Calls:**

- `Console`
- `TaskQueue`
- `console.log`
- `evaluate_task`
- `execute_tool`
- `log_error`
- `run_daemon`
- `run_schedule`
- `scan_and_diff`
- `schedule.every`
- `schedule.every(30).seconds.do`
- `schedule.run_pending`
- `task_queue.enqueue`
- `task_queue.get_next`
- `task_queue.is_empty`
- `task_queue.retry`
- `time.sleep`


## GremlinGPT/agent_core/heuristics.py

**Calls:**

- `psutil.cpu_percent`
- `psutil.virtual_memory`
- `random.random`


## GremlinGPT/agent_core/task_queue.py

**Calls:**

- `deque`
- `len`
- `range`
- `str`
- `task_queue.append`
- `task_queue.popleft`
- `task_status.items`
- `uuid.uuid4`


## GremlinGPT/agent_core/tool_executor.py

**Calls:**

- `ValueError`
- `asyncio.run`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `encode`
- `evaluate_result`
- `generate_signals`
- `get_dom_html`
- `inject_feedback`
- `log_event`
- `log_reward`
- `logger.error`
- `logger.info`
- `package_embedding`
- `run_shell_command`
- `str`
- `task.get`
- `vec.tolist`


## GremlinGPT/agent_shell/shell_executor.py

**Calls:**

- `LOG_PATH.parent.mkdir`
- `Path`
- `datetime.now`
- `datetime.now().isoformat`
- `json.dumps`
- `log.write`
- `open`
- `package_embedding`
- `result.stderr.strip`
- `result.stdout.strip`
- `shlex.split`
- `subprocess.run`


## GremlinGPT/agents/planner_agent.py

**Calls:**

- `analyze_rewards`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `enqueue_next`
- `global_queue.dump`
- `global_queue.enqueue`
- `len`
- `logger.info`
- `logger.success`
- `plan_next_task`
- `planner_loop`
- `random.choices`
- `range`
- `top_rewarded_tasks`


## GremlinGPT/backend/api/chat_handler.py

**Calls:**

- `commands.execute_command`
- `commands.parse_command`
- `data.get`
- `encode`
- `jsonify`
- `package_embedding`
- `request.get_json`
- `tokenize`


## GremlinGPT/backend/api/memory_api.py

**Calls:**

- `get_all_embeddings`
- `jsonify`


## GremlinGPT/backend/api/planner.py

**Calls:**

- `Blueprint`
- `G.add_edge`
- `G.add_node`
- `enumerate`
- `jsonify`
- `nx.DiGraph`
- `planner_bp.route`
- `request.json.get`
- `task_queue.global_queue.dump`
- `time.time`


## GremlinGPT/backend/api/scraping_api.py

**Calls:**

- `data.get`
- `enqueue_task`
- `jsonify`
- `request.get_json`


## GremlinGPT/backend/globals.py

**Calls:**

- `CFG['hardware'].get`
- `Path`
- `Path(os.path.expanduser(CFG['paths']['base_dir'])).resolve`
- `json.load`
- `load_config`
- `load_memory_config`
- `logger.add`
- `logger.info`
- `open`
- `os.path.expanduser`
- `p.replace`
- `resolve_path`
- `str`
- `toml.load`


## GremlinGPT/backend/interface/commands.py

**Calls:**

- `cmd_text.split`
- `enqueue_task`


## GremlinGPT/backend/router.py

**Calls:**

- `app.add_url_rule`


## GremlinGPT/backend/scheduler.py

**Calls:**

- `print`
- `schedule.every`
- `schedule.every(15).minutes.do`
- `schedule.run_pending`
- `time.sleep`


## GremlinGPT/backend/server.py

**Calls:**

- `Flask`
- `SocketIO`
- `app.route`
- `eventlet.monkey_patch`
- `logger.add`
- `logger.info`
- `register_routes`
- `socketio.run`


## GremlinGPT/backend/state_manager.py

**Calls:**

- `json.dump`
- `json.load`
- `open`
- `os.path.exists`


## GremlinGPT/core/kernel.py

**Calls:**

- `'\n'.join`
- `Path`
- `apply_patch`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `diff_texts`
- `embed_text`
- `f.read`
- `f.write`
- `inject_feedback`
- `logger.error`
- `logger.info`
- `logger.success`
- `open`
- `package_embedding`
- `patch_from_text`
- `read_file`
- `str`
- `test_patch.strip`
- `write_file`


## GremlinGPT/core/loop.py

**Calls:**

- `boot_loop`
- `check_trigger`
- `clear_trigger`
- `fsm.fsm_loop`
- `logger.error`
- `logger.info`
- `logger.warning`
- `time.sleep`


## GremlinGPT/core/snapshot.py

**Calls:**

- `'\n'.join`
- `Path`
- `Path(file_path).read_text`
- `Path(file_path).write_text`
- `SNAPSHOT_ROOT.mkdir`
- `content.encode`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `diff_texts`
- `embed_text`
- `f.read`
- `file.exists`
- `file.read_text`
- `full_path.relative_to`
- `hashlib.sha256`
- `hashlib.sha256(content.encode()).hexdigest`
- `hashlib.sha256(f.read()).hexdigest`
- `json.dump`
- `json.load`
- `logger.error`
- `logger.info`
- `logger.success`
- `logger.warning`
- `open`
- `os.walk`
- `package_embedding`
- `rollback`
- `sha256_file`
- `snapshot_file`
- `str` 

## GremlinGPT/executors/python_executor.py

**Calls:**

- `EXEC_LOG_DIR.mkdir`
- `Path`
- `f.write`
- `logger.error`
- `logger.info`
- `open`
- `os.remove`
- `out.write`
- `print`
- `result.stderr.strip`
- `result.stdout.strip`
- `run_python_sandbox`
- `script_path.exists`
- `str`
- `subprocess.run`
- `uuid.uuid4`


## GremlinGPT/memory/log_history.py

**Calls:**

- `HISTORY_DIR.mkdir`
- `Path`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `f.readlines`
- `f.write`
- `json.dumps`
- `json.loads`
- `load_history`
- `log_event`
- `logger.error`
- `logger.info`
- `open`
- `print`


## GremlinGPT/memory/vector_store/embedder.py

**Calls:**

- `SentenceTransformer`
- `_write_to_disk`
- `json.dump`
- `list`
- `logger.info`
- `memory_vectors.values`
- `model.encode`
- `open`
- `os.makedirs`
- `os.path.join`
- `str`
- `uuid.uuid4`
- `vector.tolist`


## GremlinGPT/nlp_engine/diff_engine.py

**Calls:**

- `diff_texts`
- `encode_text`
- `f1.read`
- `f2.read`
- `float`
- `list`
- `new.splitlines`
- `np.linalg.norm`
- `old.splitlines`
- `open`
- `semantic_similarity`
- `unified_diff`


## GremlinGPT/nlp_engine/mini_attention.py

**Calls:**

- `norm.tolist`
- `np.dot`
- `np.linalg.norm`


## GremlinGPT/nlp_engine/parser.py

**Calls:**

- `get_pos_tags`
- `tokenize`


## GremlinGPT/nlp_engine/pos_tagger.py

**Calls:**

- `nltk.download`
- `pos_tag`
- `word_tokenize`


## GremlinGPT/nlp_engine/semantic_score.py

**Calls:**

- `float`
- `np.array`
- `util.cos_sim`


## GremlinGPT/nlp_engine/tokenizer.py

**Calls:**

- `AutoTokenizer.from_pretrained`
- `tokenizer.tokenize`


## GremlinGPT/nlp_engine/transformer_core.py

**Calls:**

- `AutoModel.from_pretrained`
- `model`
- `model.eval`
- `output.last_hidden_state.mean`
- `output.last_hidden_state.mean(dim=1).squeeze`
- `output.last_hidden_state.mean(dim=1).squeeze().numpy`
- `tokenizer`
- `torch.no_grad`


## GremlinGPT/run/module_tracer.py

**Calls:**

- `'\n'.join`
- `Table`
- `f.readlines`
- `file.endswith`
- `line.strip`
- `line.strip().startswith`
- `open`
- `os.path.join`
- `os.walk`
- `path.replace`
- `path.replace('/', '.').replace`
- `print`
- `table.add_column`
- `table.add_row`
- `trace_calls`


## GremlinGPT/run/ngrok_launcher.py

**Calls:**

- `config.get`
- `config.get('ngrok', {}).get`
- `config['ngrok'].get`
- `exit`
- `img.save`
- `ngrok.connect`
- `ngrok.set_auth_token`
- `print`
- `qrcode.make`
- `str`
- `toml.load`


## GremlinGPT/scraper/dom_navigator.py

**Calls:**

- `BeautifulSoup`
- `soup.find_all`
- `soup.get_text`


## GremlinGPT/scraper/page_simulator.py

**Calls:**

- `embed_text`
- `extract_dom_structure`
- `logger.info`
- `package_embedding`


## GremlinGPT/scraper/playwright_handler.py

**Calls:**

- `async_playwright`
- `browser.close`
- `browser.new_page`
- `p.chromium.launch_persistent_context`
- `page.content`
- `page.goto`


## GremlinGPT/scraper/scraper_loop.py

**Calls:**

- `asyncio.run`
- `asyncio.sleep`
- `fetch_task`
- `get_dom_html`
- `logger.error`
- `logger.info`
- `run_scraper`
- `store_scrape_to_memory`


## GremlinGPT/self_mutation_watcher/mutation_daemon.py

**Calls:**

- `logger.error`
- `logger.info`
- `logger.warning`
- `notify_dashboard`
- `requests.post`
- `scan_and_diff`
- `t.start`
- `threading.Thread`
- `time.sleep`


## GremlinGPT/self_mutation_watcher/watcher.py

**Calls:**

- `'\n'.join`
- `Path`
- `SNAPSHOT_DIR.mkdir`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `embed_text`
- `f.read`
- `generate_diff`
- `get_snapshot_path`
- `hashlib.sha256`
- `hashlib.sha256(f.read()).hexdigest`
- `inject_feedback`
- `list`
- `load_snapshot`
- `logger.info`
- `logger.success`
- `new.splitlines`
- `old.splitlines`
- `open`
- `package_embedding`
- `save_snapshot`
- `scan_and_diff`
- `snap_path.exists`
- `snap_path.read_text`
- `snap_path.write_text`
- `unified_diff`


## GremlinGPT/self_training/feedback_loop.py

**Calls:**

- `LOG_PATH.mkdir`
- `Path`
- `TRIGGER_FILE.exists`
- `TRIGGER_FILE.unlink`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `json.dump`
- `logger.debug`
- `logger.error`
- `logger.info`
- `logger.success`
- `open`


## GremlinGPT/self_training/generate_dataset.py

**Calls:**

- `any`
- `entries.append`
- `f.readlines`
- `file.endswith`
- `line.strip`
- `open`
- `os.listdir`
- `os.path.join`


## GremlinGPT/self_training/mutation_engine.py

**Calls:**

- `mutated.append`
- `original.replace`


## GremlinGPT/self_training/trainer.py

**Calls:**

- `LogEventHandler`
- `Observer`
- `event.src_path.endswith`
- `extract_training_data`
- `json.dump`
- `logger.info`
- `mutate_dataset`
- `observer.join`
- `observer.schedule`
- `observer.start`
- `observer.stop`
- `open`
- `time.sleep`
- `trigger_retrain`
- `watch_logs`


## GremlinGPT/tests/test_dashboard.py

**Calls:**

- `requests.get`
- `requests.post`
- `res.json`


## GremlinGPT/tests/test_memory.py

**Calls:**

- `embed_text`
- `len`
- `package_embedding`


## GremlinGPT/tests/test_nlp.py

**Calls:**

- `any`
- `encode`
- `get_pos_tags`
- `tokenize`
- `vector_diff`


## GremlinGPT/tests/test_scraper.py

**Calls:**

- `asyncio.run`
- `extract_dom_structure`
- `get_dom_html`
- `html.lower`
- `len`
- `store_scrape_to_memory`


## GremlinGPT/tools/reward_model.py

**Calls:**

- `Path`
- `REWARD_LOG.parent.mkdir`
- `datetime.utcnow`
- `datetime.utcnow().isoformat`
- `evaluate_result`
- `f.write`
- `json.dumps`
- `json.loads`
- `len`
- `line.strip`
- `log_reward`
- `logger.error`
- `logger.info`
- `open`
- `output_text.lower`
- `output_text.strip`
- `print`
- `records.append`
- `round`
- `semantic_similarity`
- `sorted`
- `top_rewarded_tasks`


## GremlinGPT/trading_core/portfolio_tracker.py

**Calls:**

- `PORTFOLIO_FILE.exists`
- `Path`
- `json.dump`
- `json.load`
- `load_portfolio`
- `open`
- `save_portfolio`


## GremlinGPT/trading_core/rules_engine.py

*No calls detected.*


## GremlinGPT/trading_core/signal_generator.py

**Calls:**

- `apply_signal_rules`
- `get_live_penny_stocks`
- `logger.info`
- `package_embedding`
- `signals.append`


## GremlinGPT/trading_core/stock_scraper.py

**Calls:**

- `random.uniform`
- `round`


## GremlinGPT/trading_core/tax_estimator.py

**Calls:**

- `round`


