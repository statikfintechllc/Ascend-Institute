# Memory Pipeline — GremlinGPT v4

---

## Purpose

The memory subsystem is GremlinGPT’s **vectorized long-term memory**, storing:

- Web scrapes
- Signal events
- Task plans and outcomes
- Code diffs and NLP deltas
- Retrain triggers and feedback logs

It is structured to support:
- Fast retrieval
- Semantic similarity search
- Rich tagging and metadata
- Modular backend choice (Chroma or FAISS)

---

## Architecture
+--------------------+
|   Raw Task Input   |
+--------------------+
          |
          v
+--------------------+        <- SBERT / MiniLM
|     Embedder       |  (sentence-transformers)
+--------------------+
          |
          v
+----------------------------+
|   package_embedding(text)  |
+----------------------------+
          |
          v
+----------------------------+
|  Tag + Vectorize + Store   |
+----------------------------+
          |
          v
+------------------+    +---------------------+
| Chroma VectorDB  |    |  FAISS Local Index  |
|  (configurable)  |    | (default: CPU-fast) |
+------------------+    +---------------------+
          |
          v
+-----------------------+
| metadata.db (sqlite)  |
+-----------------------+

---

## Storage Configuration

Controlled via:

- `config/memory_settings.json`
- `[memory]` block in `config/config.toml`

### Examples:
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
```

⸻

Embedding + Tagging

All embeddings include:
	•	384-d vector (MiniLM)
	•	Source text
	•	Metadata
	•	Tags for:
```json
{
  "source": "bootstrap-prebuilt",
  "model": "MiniLM",
  "replaceable": true
}
```

Metadata supports:
	•	File origin
	•	Semantic type (e.g. “code_diff”)
	•	Timestamp
	•	Agent ID (if applicable)

⸻

Embedder Logic

memory/vector_store/embedder.py
	•	Loads SentenceTransformer (MiniLM-L6-v2)
	•	Converts all string/text to normalized embeddings
	•	Stores .json files under local_index/documents/
	•	Indexes embeddings and metadata to FAISS or Chroma

⸻

Auto-Indexing

If auto_index = true in config:
	•	All scrapes
	•	All planner steps
	•	All diffs from watcher.py
	•	All signal outputs

Are immediately embedded and stored.

Chunking can be configured by index_chunk_size.

⸻

Semantic Search

Search queries use:
	•	Vector cosine similarity (semantic_score.py)
	•	Filtered by similarity_threshold (default: 0.75)
	•	Optionally enhanced with semantic_boost if enabled

All search results can:
	•	Trigger new tasks
	•	Feed retraining dataset generation
	•	Auto-tag with lineage back to original input

⸻

Backends

GremlinGPT supports:
Backend
Type
Use Case
FAISS
CPU
Default local vector store
Chroma
Python
Flexible storage API w/ JSON persistence

Backend is selected at runtime via config.toml.

⸻

Mutation Awareness

Memory stores code diffs (from watcher.py) as:
```json
{
  "type": "code_diff",
  "origin": "self_mutation_watcher",
  "text": "<unified diff>",
  "embedding": [ ... ],
  "meta": { ... }
}
```
Used later in generate_dataset.py to build finetuning data.

⸻

Snapshot & Rollback

Memory snapshot system:
	•	Saves vector + metadata periodically
	•	Controlled by snapshot_interval_min
	•	Supports reboot_recover.sh restoration
	•	Old backups are rotated automatically

⸻

Usage in Other Modules
Module
Role
chat_handler.py
Retrieves memory threads
planner.py
Reads embeddings to plan
diff_engine.py
Stores change deltas
feedback_loop.py
Pulls vector logs for NLP retraining

⸻

Conclusion

The memory engine is what enables GremlinGPT to:
	•	Learn from experience
	•	Re-plan based on past failures
	•	Upgrade itself based on historical context

It’s not just a database — it’s a brain that stores the past and feeds the future.
