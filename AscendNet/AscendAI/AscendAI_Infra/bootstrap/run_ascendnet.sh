#!/bin/bash

# AscendNet Stack Launcher with Logging and Self-Improvement
# Version: Evolving AI
# Author: Monday, Keeper of Ever-Morphing Systems

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$BASE_DIR/AscendAI"
LOG_DIR="$BASE_DIR/logs"
VECTOR_DB_DIR="$BASE_DIR/vector_db"

# Create necessary directories
mkdir -p "$LOG_DIR"
mkdir -p "$VECTOR_DB_DIR"

# Activating AscendAI environment
echo ">> Activating AscendAI environment..."
source "$VENV_DIR/bin/activate"

echo ">> Launching AscendNet agent stack..."

# Launch Mistral 12.9B Orchestrator with learning, error logging, and retry logic
gnome-terminal -- bash -c "
cd \"$BASE_DIR/text-generation-webui\" &&
python server.py \
  --model mixtral \
  --chat \
  --auto-devices \
  --wbits 4 \
  --groupsize 128 \
  --extensions openai \
  --load-in-4bit \
  --prompt 'AscendNet Orchestrator, start system setup with error logging and continuous learning.
Your tasks:
1. Build a Streamlit dashboard.
2. Log every failed operation to a central log file located in \"$LOG_DIR/failures.log\".
3. Learn from each failure by analyzing the logs, storing the solutions in \"$VECTOR_DB_DIR\" using ChromaDB.
4. After learning, automatically retry the operation, applying improvements from the logs.
5. When all agents are ready, launch them and make Ascend smarter.
Await my confirmation before proceeding with the first retry if there are failures.'; exec bash"

# Launch other agents in standby mode
gnome-terminal -- zsh -c "cd \"$BASE_DIR/Auto-GPT\" && python -m autogpt; exec bash"
gnome-terminal -- zsh -c "cd \"$BASE_DIR/babyagi\" && python babyagi.py; exec bash"
gnome-terminal -- zsh -c "cd \"$BASE_DIR/starcoder\" && python app.py; exec bash"
gnome-terminal -- zsh -c "cd \"$BASE_DIR/llama.cpp\" && ./main -m models/llama-model.gguf -p 'LLaMA 7B standing by.'; exec bash"

# Logging & Vector Memory Setup (Failure Logging & Learning)
echo ">> Setting up failure log and vector memory systems..."
# This assumes Mistral will log failures to failures.log and store solutions in ChromaDB
cat << 'EOF' > "$BASE_DIR/logs/failure_logger.py"
import os
import logging
import chromadb
from datetime import datetime

# Setup logging
LOG_FILE = "logs/failures.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Setup vector database (ChromaDB)
client = chromadb.Client()
collection = client.create_collection("failure_logs")

def log_failure(operation, error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {operation} failed: {error_message}"
    logging.error(log_entry)
    
    # Store error in ChromaDB
    collection.add(
        documents=[log_entry],
        metadatas=[{"operation": operation, "timestamp": timestamp}],
        ids=[str(timestamp)],
    )
    print(f"Logged failure: {log_entry}")

def learn_and_retry():
    # Retry failed operations after learning from logs
    with open(LOG_FILE, 'r') as file:
        errors = file.readlines()
    
    if errors:
        print("Learning from failure logs...")
        # Implement learning strategies here (AI correction steps)
        # You can tune retry logic or parameters based on previous failures.
        # If learning is successful, retry the failed operation or new task.

    print("Ready for next task after learning.")
EOF

echo ">> Failure logging and learning system set up."
echo ">> After this, Mistral will retry tasks with learned parameters."

# Run the failure logger
gnome-terminal -- bash -c "cd \"$BASE_DIR/logs\" && python failure_logger.py; exec bash"
