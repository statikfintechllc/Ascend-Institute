#!/bin/bash

echo "[INSTALL] AscendAI Cross-Platform Bootstrap Starting..."

# Move to the repo root
cd "$(dirname "$0")"/..

# Identify OS
OS="$(uname -s)"
WINDOWS=false

# Expand detection: Linux, Mac, WSL, Git Bash, MinGW, MSYS
if [[ "$OS" =~ MINGW || "$OS" =~ MSYS || "$OS" =~ CYGWIN || "$OS" == "Windows_NT" ]]; then
  WINDOWS=true
elif [[ "$OS" == "Darwin" ]]; then
  MAC=true
elif [[ "$OS" == "Linux" ]]; then
  LINUX=true
else
  echo "[ERROR] Unsupported platform: $OS"
  exit 1
fi

# Create essential directories
mkdir -p ascend_logs task_queue

# Set executable permissions
chmod +x bootstrap/Neo.sh
chmod +x Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py

# ------------- Linux / Mac -------------
if [[ "$WINDOWS" == false ]]; then
  # Require sudo for env install
  if [[ $EUID -ne 0 ]]; then
    echo "[ERROR] Please run this script as root (use sudo)."
    exit 1
  fi

  echo "[ENV] Installing Conda environment..."
  conda env create -f ascendenv.yml || conda env create -f ascend_env.yml

  # Optional: Download model weights
  if [ -f llama_weights_and_models.sh ]; then
    echo "[MODEL] Installing LLaMA model weights..."
    bash llama_weights_and_models.sh
  fi

  # Copy Linux desktop launcher
  if [ -f bootstrap/AscendAI.desktop ]; then
    cp bootstrap/AscendAI.desktop ./AscendAI.desktop
    chmod +x ./AscendAI.desktop
    echo "[LAUNCHER] AscendAI.desktop ready in project root."
  fi

  echo "[INSTALL COMPLETE] You may now double-click AscendAI.desktop or run ./bootstrap/Neo.sh manually."

  read -p "Run Neo now? [Y/n]: " CONFIRM
  [[ "$CONFIRM" != "n" ]] && ./bootstrap/Neo.sh

# ------------- Windows (Git Bash / WSL) -------------
else
  echo "[ENV] Windows detected (Git Bash, WSL, or similar)."

  if [ -f bootstrap/launch_matrix.bat ]; then
    cp bootstrap/launch_matrix.bat ./Launch_Ascend.bat
    echo "[LAUNCHER] Windows .bat launcher deployed."
  fi

  echo "[INSTALL COMPLETE] Double-click Launch_Ascend.bat to begin or run Neo manually via Git Bash."
fi
