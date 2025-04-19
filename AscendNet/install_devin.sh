#!/bin/bash

# Use from inside your AscendNet repo
# chmod +x install_devin.sh
# ./install_devin.sh

set -euo pipefail

DEVIN_DIR="./OpenDevin"

echo ">>> Navigating to Devin project directory..."
cd "$DEVIN_DIR"

echo ">>> Checking Conda installation..."
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

eval "$(conda shell.bash hook)"
echo ">>> Creating Conda environment 'opendevin' with Python 3.11..."
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

echo ">>> Launching GUI (interactive)..."
npm run dev --prefix frontend
read -p "Launch backend now? [Y/n]: " LAUNCH_BACKEND
if [[ "$LAUNCH_BACKEND" != "Y" ]]; then
    echo ">>> Running Devin backend..."
    make run
fi