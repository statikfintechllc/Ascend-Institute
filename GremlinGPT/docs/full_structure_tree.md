<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/GremlinGPT-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

  <div align="center">
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>
</div>

# GremlinGPT v1.0.3

*Full Shell in ~3 weeks, Debug Continues*

```text
GremlinGPT/
│
├── install.sh
├── reboot_recover.sh
│
├── config/
│   │
│   ├── memory_settings.json
│   └── config.toml
│
├── conda_envs/
│   │
│   ├── gremlin-nlp.yml
│   ├── gremlin-dashboard.yml
│   ├── gremlin-scraper.yml
│   ├── gremlin-memory.yml
│   ├── gremlin-orchestrator.yml
│   └── create_envs.sh
│
├── run/
│   │
│   ├── start_all.sh
│   ├── stop_all.sh
│   ├── reboot_recover.sh
│   ├── module_tracer.py
│   ├── ngrok_launcher.py
│   ├── logs/
│   │   │
│   │   ├── runtime.log
│   │   ├── fsm.out
│   │   ├── backend.out
│   │   ├── scraper.out
│   │   └── trainer.out
│   │
│   └── checkpoints/
│       │
│       ├── state_snapshot.json
│       └── snapshots/
│
├── systemd/
│   │
│   └── gremlin.service
│
├── frontend/
│   │
│   ├── index.html
│   ├── app.js
│   ├── service-worker.js
│   ├── manifest.json
│   ├── components/
│   │   │
│   │   ├── App_Icon_&_Loading_&_Inference_Image.png
│   │   └── Background_Image_For_App.png
│   └── components/
│       │
│       ├── ChatInterface.js
│       ├── TaskTreeView.js
│       ├── MemoryGraph.js
│       └── TradingPanel.js
│
├── backend/
│   │
│   ├── server.py
│   ├── router.py
│   ├── state_manager.py
│   ├── scheduler.py
│   ├── globals.py
│   ├── interface/
│   │   │
│   │   └── commands.py
│   │
│   ├── utils/
│   │   │
│   │   └── git_ops.py
│   │
│   └── api/
│       │
│       ├── chat_handler.py
│       ├── memory_api.py
│       ├── scraping_api.py
│       └── planner.py
│
├── memory/
│   │
│   ├── vector_store/
│   │   │
│   │   ├── faiss/
│   │   │    └── ...    # fiass embeddings here
│   │   │
│   │   ├── chroma/
│   │   │    └── ...    # chroma embeddings here
│   │   │
│   │   └── embedder.py
│   │
│   ├── log_history.py
│   │
│   └── local_index/
│       │
│       ├── documents/
│       ├── scripts/
│       └── metadata.db
│
├── nlp_engine/
│   │
│   ├── tokenizer.py
│   ├── parser.py
│   ├── pos_tagger.py
│   ├── semantic_score.py
│   ├── transformer_core.py
│   ├── diff_engine.py
│   └── mini_attention.py
│
├── self_training/
│   │
│   ├── trainer.py
│   ├── generate_dataset.py
│   ├── mutation_engine.py
│   └── feedback_loop.py
│
├── scraper/
│   │
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
│   │   │
│   │   └── cookies/
│   │
│   └── profiles/
│       │
│       ├── safari_profiles/
│       │     └── ...    # Safari Profiles here
│       │
│       ├── firefox_profiles/
│       │     └── ...    # Firefox Profiles here
│       │
│       └── chromium_profile/
│             └── ...    # Chromium Profiles here
├── agent_core/
│   │
│   ├── fsm.py
│   ├── task_queue.py
│   ├── heuristics.py
│   ├── tool_executor.py
│   ├── agent_profiles.yaml
│   ├── agent_profiles.py
│   └── error_log.py
│
├── trading_core/
│   │
│   ├── signal_generator.py
│   ├── stock_scraper.py
│   ├── rules_engine.py
│   ├── portfolio_tracker.py
│   └── tax_estimator.py
│
├── agents/
│   │
│   └── planner_agent.py
│
├── core/
│   │
│   ├── loop.py
│   ├── kernel.py
│   └── snapshot.py
│
├── executors/
│   │
│   └── python_executor.py
│
├── tools/
│   │
│   └── reward_model.py
│
├── agent_shell/
│   │
│   └── shell_executor.py
│
├── self_mutation_watcher/
│   │
│   ├── watcher.py
│   └── mutation_daemon.py
│
├── data/
│   │
│   ├── prompts/
│   │   │
│   │   ├── README.md
│   │   └── ...    # System prompts here
│   │
│   ├── raw_scrapes/
│   │   │
│   │   └── ...    # Raw scrap data here
│   ├── embeddings/
│   │   │
│   │   └── ...    # Embedding here
│   ├── nlp_training_sets/
│   │   │   
│   │   └── bootstrap.json
│   │   
│   └── logs/
│       │   
│       ├── bootstrap.log
│       ├── gremlin_exec_log.jsonl
│       └── rewards.jsonl
│
├── tests/
│   │   
│   ├── test_scraper.py
│   ├── test_memory.py
│   ├── test_nlp.py
│   └── test_dashboard.py
│
├── dev-experiment/
│   │  
│   ├── memory_hacking/
│   │   │   
│   │   ├── inject_custom_embeddings.py
│   │   ├── override_reward_trace.py
│   │   ├── memory_probe_tool.py
│   │   └── README.md
│   │
│   ├── new_agents/
│   │   │   
│   │   ├── planning/
│   │   │   │
│   │   │   ├── speculative_planner.py
│   │   │   └── scratchpad_agent.py
│   │   ├── self_reflection/
│   │   │   │
│   │   │   ├── hallucination_guard.py
│   │   │   └── anomaly_analyzer.py
│   │   ├── loop_extensions/
│   │   │   │
│   │   │   ├── fsm_tick_debugger.py
│   │   │   └── dynamic_interval_mutator.py
│   │   └── README.md
│   │
│   ├── broken_scrapers/
│   │   │
│   │   ├── discord_leaks_scraper.py
│   │   ├── legacy_twitter_collector.py
│   │   ├── unstable_playwright_agent.py
│   │   └── README.md
│   │
│   └── your_mutations_here.md
│
├── docs/
│   │
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
├── demos/
│   │
│   └── README.md
│
├── utils/
│   │
│   └── nltk_setup.py
│
└── README.md
```
