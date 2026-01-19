# Memory Module

The `memory` module provides persistent storage, vector embeddings, and knowledge management for GremlinGPT's long-term memory and learning capabilities.

## Components

### 📚 log_history.py
**Event Logging and History**
- Comprehensive event logging system
- Historical data preservation
- Event categorization and indexing
- Query and retrieval mechanisms

### 📁 vector_store/
**Vector Storage and Embeddings**
- High-dimensional vector storage
- Semantic embedding generation
- Similarity search and retrieval
- Vector indexing and optimization

#### embedder.py
- Text-to-vector conversion
- Multi-modal embedding support
- Embedding model management
- Batch processing capabilities

### 📁 local_index/
**Local Knowledge Indexing**
- Local file system indexing
- Knowledge graph construction
- Relationship mapping
- Fast local search capabilities

## Architecture

```text
┌─────────────────┐    ┌─────────────────┐
│   Log History   │────│  Vector Store   │
│   (Events)      │    │ (Embeddings)    │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┼
                                 │
                    ┌─────────────────┐
                    │  Local Index    │
                    │ (Knowledge KB)  │
                    └─────────────────┘
```

## Key Features

- **Persistent Memory**: Long-term information retention
- **Semantic Search**: Vector-based similarity matching  
- **Event Tracking**: Comprehensive system history
- **Knowledge Graphs**: Relationship mapping and discovery
- **Scalable Storage**: Efficient data organization
