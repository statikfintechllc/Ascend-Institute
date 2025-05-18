#!/bin/bash

echo "===[ GREMLIN SYSTEM BOOT TEST ]==="
echo "[1/6] Activating environments..."

conda activate gremlin-nlp && echo "✓ NLP env ready"
conda activate gremlin-memory && echo "✓ Memory env ready"
conda activate gremlin-scraper && echo "✓ Scraper env ready"
conda activate gremlin-dashboard && echo "✓ Dashboard env ready"
conda activate gremlin-orchestrator && echo "✓ Orchestrator env ready"

echo "[2/6] Running module health checks..."

echo "--- NLP ---"
python3 -c "from nlp_engine import tokenizer, transformer_core, semantic_score; print('✓ NLP modules loaded')"

echo "--- MEMORY ---"
python3 -c "from memory.vector_store import embedder; print('✓ Embedder loaded')"

echo "--- AGENT CORE ---"
python3 -c "from agent_core import fsm, task_queue; print('✓ FSM + Task Queue ready')"

echo "--- TRAINING ---"
python3 -c "from self_training import trainer, mutation_engine; print('✓ Training core modules OK')"

echo "--- SCRAPER ---"
python3 -c "from scraper import scraper_loop, dom_navigator; print('✓ Scraper initialized')"

echo "--- BACKEND ---"
python3 -c "from backend import server, router, state_manager; print('✓ Backend server modules good')"

echo "[3/6] Checking log file write access..."
touch run/logs/runtime.log && echo "✓ Log file writable"

echo "[4/6] Snapshot read/write check..."
touch run/checkpoints/test_snapshot.json && echo '{}' > run/checkpoints/test_snapshot.json && echo "✓ Checkpoint write OK"

echo "[5/6] Code watcher dry run..."
python3 self_mutation_watcher/watcher.py

echo "[6/6] Test complete."
echo "All base modules passed load test. You may now run the system."
