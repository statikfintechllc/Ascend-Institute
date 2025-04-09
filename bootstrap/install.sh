#!/bin/bash

echo "[INSTALL] Beginning AscendAI installation..."

# Elevate if not root
if [[ $EUID -ne 0 ]]; then
   echo "[WARN] This script must be run as root (use sudo)."
   exit 1
fi

# Move to repo root if not already
cd "$(dirname "$0")"/..

# Create logs and task queue dirs if missing
mkdir -p ascend_logs task_queue

# Set executable permissions
chmod +x bootstrap/Neo.sh
chmod +x Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py

# Install dependencies (assumes conda installed)
echo "[INSTALL] Installing environment via Conda..."
conda env create -f ascendenv.yml || conda env create -f ascend_env.yml

# Optional: Install LLaMA weights
if [ -f llama_weights_and_models.sh ]; then
  echo "[INSTALL] Fetching model weights..."
  bash llama_weights_and_models.sh
fi

# Run Neo
echo "[INSTALL COMPLETE] Launching Neo..."
./bootstrap/Neo.sh
