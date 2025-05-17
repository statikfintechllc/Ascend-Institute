#!/bin/bash

echo ">>> [ASCEND] Activating OpenDevin Sovereign Core..."

DEVIN_DIR="../OpenDevin"

if [ ! -d "$DEVIN_DIR" ]; then
    echo "[ERROR] OpenDevin directory not found at $DEVIN_DIR"
    exit 1
fi

cd "$DEVIN_DIR" || exit 1

# Load Conda environment
if ! command -v conda &> /dev/null; then
    echo "[ERROR] Conda not found. Please install Miniconda or Anaconda."
    exit 1
fi

eval "$(conda shell.bash hook)"
conda activate opendevin

# Ensure Conda shell is initialized
if ! grep -q 'conda initialize' ~/.bashrc; then
    echo "[FIX] Conda not initialized. Running 'conda init bash'..."
    conda init bash
    source ~/.bashrc
fi

# Ensure Conda shell is initialized
if ! grep -q 'conda initialize' ~/.bashrc; then
    echo "[FIX] Conda not initialized. Running 'conda init bash'..."
    conda init bash
    source ~/.bashrc
fi

# Check if build was run
if [ ! -f "./build_marker.txt" ]; then
    echo ">>> [DEVIN] Initializing build process..."
    make build || { echo "[ERROR] Build failed."; exit 1; }
    touch build_marker.txt
fi

# Run Devin (Ascend Core)
echo ">>> [ASCEND] Launching Devin core runtime..."
make run || { echo "[ERROR] Failed to launch Devin."; exit 1; }
