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

REQUIRED=("make" "python3" "pip" "node" "npm")  # Add more as needed
for cmd in "${REQUIRED[@]}"; do
    if ! command -v $cmd &> /dev/null; then
        echo "[ERROR] Required command '$cmd' not found. Please install it."
        exit 1
    fi
done

if [ ! -f "$DEVIN_CORE/Makefile" ] || [ ! -d "$DEVIN_CORE/src" ]; then
    echo "[ERROR] OpenDevin source structure incomplete."
    exit 1
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