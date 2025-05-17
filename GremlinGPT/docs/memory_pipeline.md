# Memory Pipeline

Memory is managed through the `embedder.py` module.

### Flow

1. Vector produced via `SentenceTransformer.encode()`
2. Stored in-memory + written to `local_index/documents/`
3. Metadata includes:
   - ID, Source, Model
   - Embedding vector (float32)
   - Tags (semantic_topic, source, content_type)

### Config Control

Settings in `memory_settings.json`:
- `auto_index`: True
- `format`: float32
- `embedding_dim`: 384
- `vector_backend`: chromadb or faiss

### Retrieval

- Used by `memory_api.graph()`
- Top-k similarity via cosine distance (`semantic_score.py`)
