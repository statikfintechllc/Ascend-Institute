#!/bin/bash

echo "======================================"
echo "   [Neo] Initiating Boot Protocol..."
echo "======================================"

# Log the boot first
mkdir -p ascend_logs
echo "[BOOT] $(date)" >> ascend_logs/boot_timestamps.log

# Initialize task queue
mkdir -p task_queue
echo "Scan memory and initialize vector DB." > task_queue/init.task

# Path to OpenDevin
DEVIN_CORE="../OpenDevin"

# Check if Devin exists
if [ ! -d "$DEVIN_CORE" ]; then
    echo "[ERROR] OpenDevin core not found in expected location: $DEVIN_CORE"
    exit 1
fi

cd "$DEVIN_CORE" || exit 1

# Activate Conda environment
if ! command -v conda &> /dev/null; then
    echo "[ERROR] Conda not found. Please install Miniconda or Anaconda."
    exit 1
fi

eval "$(conda shell.bash hook)"
conda activate opendevin

# Create default config if missing
if [ ! -f "config.toml" ]; then
    echo "[Neo] Creating default config.toml..."
    cat <<EOF > config.toml
[core]
workspace_base = "./workspace"
persist_sandbox = false
run_as_devin = true
sandbox_container_image = "custom_image"
EOF
fi

# Build Devin once if needed
if [ ! -f "./build_marker.txt" ]; then
    echo ">>> [DEVIN] First-time build..."
    make build || { echo "[ERROR] Build failed."; exit 1; }
    touch build_marker.txt
fi

# Run Devin
echo ">>> [DEVIN] Sovereign Core launching..."
make run || { echo "[ERROR] Devin launch failed."; exit 1; }

echo ">> [Neo] Systems online. Awaiting recursive chain loop."