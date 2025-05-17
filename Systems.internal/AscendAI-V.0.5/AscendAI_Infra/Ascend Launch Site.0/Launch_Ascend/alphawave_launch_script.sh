#!/bin/bash
# AlphaWave Initial Boot & Setup Script
# Purpose: Initialize environment, sync AI systems, launch Ascend AI

echo "[AlphaWave] Starting system initialization..."

# System Update
sudo apt update && sudo apt upgrade -y

# Install Miniconda (if not installed)
if ! command -v conda &> /dev/null; then
  echo "[AlphaWave] Installing Miniconda..."
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
  bash miniconda.sh -b -p $HOME/miniconda
  eval "$($HOME/miniconda/bin/conda shell.bash hook)"
  conda init
fi

# Load Conda
source ~/.bashrc

# Create and activate Ascend environment
echo "[AlphaWave] Creating Ascend AI Environment..."
conda env create -f ascendenv.yml
conda activate ascendenv

# Setup environment structure
mkdir -p ~/AscendAI/{models,agents,datasets,prompts,logs,outputs}

echo "[AlphaWave] Environment ready."
echo "[AlphaWave] You may now launch LLaMA, CrewAI, or any agents."

# Optional: Launch interface/dashboard
# streamlit run ~/AscendAI/dashboard.py
