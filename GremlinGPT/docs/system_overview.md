# System Overview

**GremlinGPT** is a fully offline, self-evolving AI orchestration system. It leverages:

- Modular FSM agents
- Local NLP stack (tokenizer + transformer + attention + scoring)
- Vector memory via FAISS/Chroma
- Feedback loops based on performance logs
- A PWA frontend to control all modules

### Primary Subsystems

| Subsystem       | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `backend/`      | REST + socket routing, config loader, and global dispatcher  |
| `agent_core/`   | FSM planner, retry logic, task queue, tool execution         |
| `scraper/`      | DOM browser with memory-backed storage                       |
| `nlp_engine/`   | Tokenizer, BERT encoder, POS tagger, semantic scorer         |
| `memory/`       | Vector embedder and tagged persistent storage                |
| `self_training/`| Mutation pipeline and auto-retraining                        |
| `trading_core/` | Penny stock signal scanner + rules engine + portfolio model  |
| `frontend/`     | Offline-first progressive dashboard                          |

All components communicate via direct Python imports and indirect file/message passing.
