<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
	
</div>

————

# GremlinGPT v1.0.2
```text
GremlinGPT/
├── README.md
├── install.sh
├── reboot_recover.sh
│
├── config/
│   ├── config.toml
│   ├── memory_settings.json
│   └── dashboard_config.yaml
│
├── conda_envs/
│   ├── gremlin-nlp.yml
│   ├── gremlin-dashboard.yml
│   ├── gremlin-scraper.yml
│   ├── gremlin-memory.yml
│   ├── gremlin-orchestrator.yml
│   └── create_envs.sh
│
├── run/
│   ├── start_all.sh
│   ├── stop_all.sh
│   ├── reboot_recover.sh
│   ├── module_tracer.py
│   ├── ngrok_launcher.py
│   ├── logs/
│   │   ├── runtime.log
│   │   ├── fsm.out
│   │   ├── backend.out
│   │   ├── scraper.out
│   │   └── trainer.out
│   └── checkpoints/
│       ├── state_snapshot.json
│       └── snapshots/
│
├── systemd/
│   └── gremlin.service
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── service-worker.js
│   ├── manifest.json
│   └── components/
│       ├── ChatInterface.js
│       ├── TaskTreeView.js
│       ├── MemoryGraph.js
│       └── TradingPanel.js
│
├── backend/
│   ├── server.py
│   ├── router.py
│   ├── state_manager.py
│   ├── scheduler.py
│   ├── globals.py
│   ├── interface/
│   │   └── commands.py
│   ├── utils/
│   │   └── git_ops.py
│   └── api/
│       ├── chat_handler.py
│       ├── memory_api.py
│       ├── scraping_api.py
│       └── planner.py
│
├── memory/
│   ├── vector_store/
│   │   ├── faiss/
│   │   ├── chroma/
│   │   └── embedder.py
│   ├── log_history.py
│   └── local_index/
│       ├── documents/
│       ├── scripts/
│       └── metadata.db
│
├── nlp_engine/
│   ├── tokenizer.py
│   ├── parser.py
│   ├── pos_tagger.py
│   ├── semantic_score.py
│   ├── transformer_core.py
│   ├── diff_engine.py
│   └── mini_attention.py
│
├── self_training/
│   ├── trainer.py
│   ├── generate_dataset.py
│   ├── mutation_engine.py
│   └── feedback_loop.py
│
├── scraper/
│   ├── scraper_loop.py
│   ├── stt_scrapper.py
│   ├── tws_scrapper.py
│   ├── source_router.py
│   ├── web_knowledge_scraper.py
│   ├── dom_navigator.py
│   ├── page_simulator.py
│   ├── ask_monday_handler.py
│   ├── playwright_handler.py
│   ├── source_router.py
│   ├── persistence/
│   │   └── cookies/
│   └── profiles/
│       └── chromium_profile/
│
├── agent_core/
│   ├── fsm.py
│   ├── task_queue.py
│   ├── heuristics.py
│   ├── tool_executor.py
│   ├── agent_profiles.yaml
│   ├── agent_profiles.py
│   └── error_log.py
│
├── trading_core/
│   ├── signal_generator.py
│   ├── stock_scraper.py
│   ├── rules_engine.py
│   ├── portfolio_tracker.py
│   └── tax_estimator.py
│
├── agents/
│   └── planner_agent.py
│
├── core/
│   ├── loop.py
│   ├── kernel.py
│   └── snapshot.py
│
├── executors/
│   └── python_executor.py
│
├── tools/
│   └── reward_model.py
│
├── agent_shell/
│   └── shell_executor.py
│
├── self_mutation_watcher/
│   ├── watcher.py
│   └── mutation_daemon.py
│
├── data/
│   ├── prompts/
│   │   └── README.md
│   ├── raw_scrapes/
│   ├── embeddings/
│   ├── nlp_training_sets/
│   │   └── bootstrap.json
│   └── logs/
│       ├── bootstrap.log
│       ├── gremlin_exec_log.jsonl
│       └── rewards.jsonl
│
├── tests/
│   ├── test_scraper.py
│   ├── test_memory.py
│   ├── test_nlp.py
│   └── test_dashboard.py
│
├── docs/
│   ├── README.md
│   ├── full_structure_tree.txt
│   ├── system_call_graph.md
│   ├── self_training.md
│   ├── system_overview.md
│   ├── fsm_architecture.md
│   ├── memory_pipeline.md
│   ├── trading_signals.md
│   ├── self_training.md
│   ├── ngrok_integration.md
│   ├── gremlin.service.md
│   └── automated_shell.md
│
└── test_system_start.sh
```
