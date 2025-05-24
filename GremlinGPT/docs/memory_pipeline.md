<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-red?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

# Memory Pipeline — GremlinGPT v1.0.2

---

## Purpose

The memory subsystem is GremlinGPT’s **vectorized long-term memory**, storing:

- Web scrapes and DOM content
- Trading signal outputs
- Task plans, priorities, outcomes
- Code diffs and NLP deltas
- Retrain triggers and mutation feedback

Memory is designed for:
- Fast semantic retrieval
- Continuous learning via vector deltas
- High-granularity tagging and lineage tracking
- Configurable backend (FAISS or ChromaDB)

Embeddings are 384-d float32 vectors optimized for CPU-based FAISS indexing by default.

---

## Architecture

The memory stack flows as:

Raw Text → SBERT MiniLM → embed_text() → package_embedding()
→ Tags + Metadata
→ Vector Store (FAISS/Chroma)
→ metadata.db (SQLite) + /documents/

---

### Core Layers:

- `embed_text()` – encodes raw input
- `package_embedding()` – stores vector + metadata
- `inject_watermark()` – tags memory state transitions
- `faiss_index/` or `chroma_db/` – vector backend
- `metadata.db` – searchable context + lineage

---

## Configuration

Memory behavior is controlled by:

- `config/config.toml` → `[memory]`
- `config/memory_settings.json` → overrides for dev/debug

### Sample `memory_settings.json`
```json
{
  "vector_backend": "faiss",
  "embedding_dim": 384,
  "auto_index": true,
  "storage": {
    "vector_store_path": "./memory/vector_store/faiss/",
    "metadata_db": "./memory/local_index/metadata.db"
  }
}


⸻

## Embedding & Tagging

Every memory entry contains:
	•	embedding: 384-dim vector from MiniLM-L6-v2
	•	text: Source text or summary
	•	meta: Dictionary with semantic keys
	•	tags: Purpose + model lineage

### Example:

{
  "id": "abc123",
  "text": "Planned task: scrape SEC filings",
  "embedding": [0.123, 0.991, ...],
  "meta": {
    "agent": "planner_agent",
    "task_type": "scrape",
    "timestamp": "2025-05-18T13:22:01Z"
  },
  "tags": {
    "source": "planner",
    "model": "MiniLM",
    "replaceable": true
  }
}


⸻

## Embedder Logic

### Located in memory/vector_store/embedder.py
	•	Loads MiniLM-L6-v2 using SentenceTransformer
	•	Normalizes and embeds all NLP or task payloads
	•	Saves .json vectors to local_index/documents/
	•	Stores FAISS index or Chroma collection as defined

### Functions:
	•	embed_text(text)
	•	package_embedding(text, vector, meta)
	•	inject_watermark(origin="...")

⸻

## Auto Indexing

### If auto_index = true in config, the following sources are automatically embedded:
	•	DOM content from scraper_loop.py
	•	Signals from signal_generator.py
	•	Task plans from planner_agent.py
	•	Mutations and diffs from watcher.py
	•	Shell outputs and NLP commands

⸻

## Semantic Search

### Semantic queries run against vector memory using:
	•	Cosine similarity via semantic_score.py
	•	Threshold from similarity_threshold (default: 0.75)
	•	Optionally enhanced via semantic_boost flag

### Matched results can:
	•	Trigger tasks (e.g. re-scrape)
	•	Seed new planner steps
	•	Feed generate_dataset.py for self-train loops

⸻

## Backends

Backend
Type
Use Case
FAISS
CPU
Default, fast local index
Chroma
JSON
Dev-friendly + persistent

### Selected in config.toml under [memory]:

[memory]
vector_backend = "faiss"
embedding_dim = 384
auto_index = true

⸻


⸻

Mutation Awareness

When FSM, planner, or kernel is mutated:
	•	Code diff is generated via diff_engine.py
	•	Stored in memory like this:

{
  "type": "code_diff",
  "origin": "self_mutation_watcher",
  "text": "<unified diff>",
  "embedding": [ ... ],
  "meta": {
    "semantic_score": 0.41,
    "lineage_id": "uuid",
    "timestamp": "..."
  }
}

These diffs are critical for generating self_train tasks and for dataset building in generate_dataset.py.

⸻

## Snapshot & Rollback

### The memory system supports temporal rollbacks via snapshotting:
	•	Periodic dumps of vector and metadata states
	•	Controlled by snapshot_interval_min in config.toml
	•	Supports reboot_recover.sh for failover or crash recovery
	•	Old backups are auto-rotated

⸻

## Integrated Modules

Module
Role
chat_handler.py
Retrieves context from memory
planner_agent.py
Picks next task via reward + memory scan
diff_engine.py
Stores semantic and code deltas
feedback_loop.py
Logs retrain triggers to memory
tool_executor.py
Embeds all tool results and signals
mutation_daemon.py
Monitors code for drift and vector deltas

⸻

## Logging & Watermarking

### Watermarking is used to:
	•	Tag mutation-aware embeddings
	•	Mark FSM transitions or kernel patch events
	•	Leave source:GremlinGPT lineage metadata

### Each inject_watermark() call adds:

{
  "origin": "fsm_loop",
  "timestamp": "2025-05-18T13:26:44Z",
  "watermark": "source:GremlinGPT"
}

⸻

## Conclusion

### The memory engine enables GremlinGPT to:
	•	Learn from past actions
	•	Replan based on reward history
	•	React to environment changes
	•	Train itself from mutation logs

### This isn’t just storage — it’s long-term cognition, replayable reasoning, and evolutionary state tracking.
