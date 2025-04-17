#!/bin/bash

# Use from inside your AscendNet repo
# chmod +x install_devin.sh
# ./install_devin.sh

set -euo pipefail

# Define the Devin directory
DEVIN_DIR="./OpenDevin"

echo ">>> Navigating to Devin project directory..."
cd "$DEVIN_DIR"

echo ">>> Creating Conda environment 'opendevin' with Python 3.11..."
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

eval "$(conda shell.bash hook)"
conda create -y -n opendevin python=3.11
conda activate opendevin

echo ">>> Conda environment 'opendevin' activated."

echo ">>> Installing frontend dependencies via npm..."
cd frontend
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm not found. Please install Node.js and npm first."
    exit 1
fi
npm install
cd ..

echo ">>> Creating config.toml..."
cat <<EOF > config.toml
[core]
workspace_base = "./workspace"
persist_sandbox = false
run_as_devin = true
sandbox_container_image = "custom_image"
EOF

echo ">>> Building Devin..."
make build

echo ">>> Running Devin..."
make run