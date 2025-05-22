#!/bin/zsh

echo "[BOOT] Injecting GremlinGPT watermark to system trace."
echo "Boot ID: $(uuidgen) | Source: GremlinGPT | Time: $(date -u)" >> /var/log/gremlin_boot_trace.log
echo "[START] Initializing GremlinGPT System..."

source ~/.zshrc

# Start NLP & Memory Services (embedder/transformer)
echo "[START] Activating gremlin-nlp..."
conda activate gremlin-nlp || exit 1

# Start Backend
echo "[START] Launching backend server..."
conda activate gremlin-dashboard && \
  nohup python backend/server.py > run/logs/backend.out 2>&1 &

# Start FSM Agent Core
echo "[START] Launching FSM..."
conda activate gremlin-orchestrator && \
  nohup python agent_core/fsm.py > run/logs/fsm.out 2>&1 &

# Start Scraper
echo "[START] Launching Web Scraper..."
conda activate gremlin-scraper && \
  nohup python scraper/scraper_loop.py > run/logs/scraper.out 2>&1 &

# Start Trainer
echo "[START] Launching Self-Trainer..."
conda activate gremlin-orchestrator && \
  nohup python self_training/trainer.py > run/logs/trainer.out 2>&1 &

# Launch dashboard backend
echo "[*] Starting backend server..."
conda activate gremlin-dashboard
  nohub python backend/server.py &

# Launch ngrok tunnel if enabled
echo "[*] Checking ngrok..."
  nohub python run/ngrok_launcher.py

echo "[START] All subsystems running."

