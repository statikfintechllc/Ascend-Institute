# METADATA_DB_PATH Configuration Alignment

## Overview
This document outlines the changes made to align all GremlinGPT modules to use `METADATA_DB_PATH` from config for metadata operations, eliminating hardcoded paths and ensuring consistent configuration management.

## Changes Made

### 1. Backend Configuration (backend/globals.py)
- **Added comprehensive path exports** from config.toml:
  - `METADATA_DB_PATH`: Central metadata store path
  - `VECTOR_STORE_PATH`: Main vector store directory
  - `FAISS_PATH`: FAISS-specific storage
  - `CHROMA_PATH`: Chroma-specific storage  
  - `LOCAL_INDEX_PATH`: Local document index
  - `LOCAL_DB`: Local database file
  - `FAISS_INDEX_FILE`: FAISS index file
  - `CHROMA_DB`: Chroma database file

- **Added documentation** explaining the role and usage of `METADATA_DB_PATH`
- **Centralized path resolution** using the existing `resolve_path()` function

### 2. Memory Embedder (memory/vector_store/embedder.py)
- **Removed direct config loading** from config.toml and memory.json
- **Updated to import all paths** from `backend.globals`
- **Added fallback mechanism** for import failures
- **Updated documentation** to reference config-driven approach
- **Maintained backward compatibility** with existing function interfaces

### 3. Backend Commands (backend/interface/commands.py)
- **Updated path imports** to use `backend.globals`
- **Added fallback paths** for error scenarios
- **Maintained existing storage configuration** compatibility
- **Updated module logging** to reflect new source

### 4. Learning Agent (agents/learning_agent.py)
- **Removed hardcoded path** `"memory/learning_models"`
- **Updated to use** `MODELS_DIR` from config via `backend.globals`
- **Dynamic path construction** using `Path(MODELS_DIR) / "learning_models"`

### 5. Configuration Cleanup (config/memory.json)
- **Removed duplicate path entries**:
  - `vector_store_path`
  - `local_index_path` 
  - `metadata_db`
- **Maintained storage flags** and other configuration
- **Eliminated config duplication** between config.toml and memory.json

## Configuration Sources

### Primary Source: config.toml
All file and directory paths are now managed in `config.toml` under the `[paths]` section:

```toml
[paths]
metadata_db = "$ROOT/memory/local_index/metadata.db"
vector_store_path = "$ROOT/memory/vector_store/"
faiss_path = "$ROOT/memory/vector_store/faiss/"
chroma_path = "$ROOT/memory/vector_store/chroma/"
local_index_path = "$ROOT/memory/local_index/documents/"
local_db = "$ROOT/memory/local_index/documents.db"
```

### Secondary Source: memory.json
Only non-path configuration remains:
- Backend selection flags (`use_faiss`, `use_chroma`)
- Embedding parameters
- Search and tagging configuration
- Performance settings

## Module Usage Patterns

### Correct Usage
```python
# Import paths from backend.globals
from backend.globals import METADATA_DB_PATH, VECTOR_STORE_PATH, FAISS_PATH

# Use in your module
def store_metadata(data):
    with sqlite3.connect(METADATA_DB_PATH) as conn:
        # ... store metadata
```

### Incorrect Usage (Avoided)
```python
# Don't do this - hardcoded paths
METADATA_DB_PATH = "./memory/local_index/metadata.db"

# Don't do this - direct config loading
from backend.globals import MEM
storage_conf = MEM.get("storage", {})
metadata_path = storage_conf.get("metadata_db", "...")
```

## Modules Updated

### Core Modules
- `backend/globals.py` - Path export and documentation
- `memory/vector_store/embedder.py` - Config-driven path loading
- `backend/interface/commands.py` - Config-driven path loading

### Agent Modules  
- `agents/learning_agent.py` - Removed hardcoded learning models path

### Configuration
- `config/memory.json` - Removed duplicate path config

## Modules Using Config-Driven Paths (via embedder)

The following modules automatically benefit from config-driven paths through their imports from the updated embedder module:

### Trading Core
- `trading_core/portfolio_tracker.py`
- `trading_core/signal_generator.py` 
- `trading_core/rules_engine.py`
- `trading_core/tax_estimator.py`

### Self-Training
- `self_training/mutation_engine.py`
- `self_training/feedback_loop.py`
- `self_training/generate_dataset.py`
- `self_training/trainer.py`

### NLP Engine
- `nlp_engine/chat_session.py`
- `nlp_engine/tokenizer.py`
- `nlp_engine/pos_tagger.py`
- `nlp_engine/parser.py`
- `nlp_engine/mini_attention.py`

### Core Systems
- `core/kernel.py`
- `core/snapshot.py`
- `agent_core/fsm.py`

### API and Backend
- `backend/api/memory_api.py`
- `backend/router.py`

## Validation

### Import Testing
All key modules can import required paths from `backend.globals`:
- ✅ METADATA_DB_PATH accessible
- ✅ VECTOR_STORE_PATH accessible
- ✅ Fallback mechanisms in place
- ✅ No hardcoded "./memory/" paths in critical modules

### Configuration Consistency
- ✅ Single source of truth (config.toml)
- ✅ Eliminated duplication between config files
- ✅ Proper path resolution with $ROOT expansion
- ✅ Backward compatibility maintained

## Future Maintenance

### Adding New Modules
When creating new modules that need metadata or vector store access:

1. Import from `backend.globals`:
   ```python
   from backend.globals import METADATA_DB_PATH, VECTOR_STORE_PATH
   ```

2. Use the imported paths directly
3. Do not hardcode "./memory/" paths
4. Do not load config.toml or memory.json directly for path information

### Configuration Changes
- Update paths in `config.toml` only
- Use `$ROOT` for relative-to-project paths
- Test path resolution in development
- Verify all modules continue to function after path changes

## Benefits Achieved

1. **Centralized Configuration**: All paths managed in one location
2. **Consistency**: No more path mismatches between modules  
3. **Maintainability**: Easy to relocate storage directories
4. **Documentation**: Clear understanding of metadata usage
5. **Flexibility**: Easy to switch between different storage layouts
6. **Error Handling**: Graceful fallbacks for configuration issues

## Contact

For questions about this configuration system, refer to:
- `backend/globals.py` - Central configuration exports
- This documentation file
- GremlinGPT project maintainers