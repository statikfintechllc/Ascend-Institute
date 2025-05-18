                          generate_dataset.py
                                 ▲
                                 │
                            trainer.py
                                 ▲
                                 │
                          transformer_core.py
                                 ▲
                                 │
     tokenizer.py   ←──  fsm.py  ──→  tool_executor.py  ──→  signal_generator.py  ─→  rules_engine.py
                                 │                         │                         │
                                 │                         └──→  scraper_loop.py  ──→  playwright_handler.py
          task_queue.py  ←───────┘                                                   └──→  page_simulator.py
              ▲                                                                             ▲
              │                                                                             │
         planner.py  ─────→  router.py  ─→  chat_handler.py  ─→  commands.py                │
                                │                           └→  tokenizer.py                │
                                │                           └→  embedder.py  ─→  semantic_score.py
                                │
                                └→  memory_api.py  ─→  embedder.py
                                                        ▲
                                                        │
          TradingPanel.js  ─→  mutation_engine.py  ─→  dom_navigator.py
              ▲
              │
    frontend/app.js  ─→  ChatInterface.js
                   └→  TaskTreeView.js  ─→  embedder.py
                   └→  MemoryGraph.js   ─→  memory_api.py


--------------------------------------------------------------------------------


GremlinGPT Full Script Call Graph

Nodes:
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

Connections:
- server.py → router.py
- router.py → chat_handler.py, planner.py, scraping_api.py, memory_api.py
- chat_handler.py → commands.py, tokenizer.py, transformer_core.py, embedder.py
- planner.py → signal_generator.py, task_queue.py
- signal_generator.py → stock_scraper.py, rules_engine.py, embedder.py
- memory_api.py → embedder.py
- scraping_api.py → task_queue.py
- fsm.py → task_queue.py, tool_executor.py, heuristics.py
- tool_executor.py → scraper_loop.py, feedback_loop.py, transformer_core.py, signal_generator.py
- feedback_loop.py → embedder.py
- trainer.py → feedback_loop.py, mutation_engine.py, generate_dataset.py
- scraper_loop.py → playwright_handler.py, page_simulator.py
- page_simulator.py → dom_navigator.py, embedder.py
- app.js → ChatInterface.js, MemoryGraph.js, TaskTreeView.js, TradingPanel.js
- TradingPanel.js → planner.py
- TaskTreeView.js → fsm.py, embedder.py
- MemoryGraph.js → memory_api.py


--------------------------------------------------------------------------------


# Module Call Graph

### → backend/server.py
    ↳ router.py
    ↳ api/chat_handler.py
        ↳ tokenizer.py
        ↳ transformer_core.py
        ↳ embedder.py
    ↳ api/planner.py
        ↳ signal_generator.py
            ↳ rules_engine.py
            ↳ stock_scraper.py
        ↳ task_queue.py

### → fsm.py
    ↳ task_queue.py
    ↳ tool_executor.py
        ↳ get_dom_html()
        ↳ transformer_core.encode()
        ↳ feedback_loop.inject_feedback()
    ↳ heuristics.py

### → scraper_loop.py
    ↳ playwright_handler.py
    ↳ dom_navigator.py
    ↳ page_simulator.py
        ↳ embedder.py

### → trainer.py
    ↳ watchdog
    ↳ generate_dataset.py
    ↳ mutation_engine.py
    ↳ feedback_loop.py

### → frontend/app.js
    ↳ ChatInterface.js → /api/chat
    ↳ TaskTreeView.js → /api/agent/tasks
    ↳ MemoryGraph.js → /api/memory/graph
    ↳ TradingPanel.js → /api/trading/signals


--------------------------------------------------------------------------------
