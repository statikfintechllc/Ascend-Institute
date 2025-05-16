#!/bin/bash

echo "[INSTALL] AscendAI Cross-Platform Bootstrap Starting..."

# Move to the repo root
cd "$(dirname "$0")"/..

# Identify OS
OS="$(uname -s)"
WINDOWS=false

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
chmod +x bootstrap/run_devin.sh
chmod +x bootstrap/launch_menu.sh
chmod +x Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py

# ----------- Linux / Mac -----------
if [[ "$WINDOWS" == false ]]; then
  if [[ $EUID -ne 0 ]]; then
    echo "[ERROR] Please run this script as root (use sudo)."
    exit 1
  fi

  echo "[ENV] Installing Conda environment..."
  conda env create -f ascendenv.yml || conda env create -f ascend_env.yml

  # Optional: Model weights
  if [ -f llama_weights_and_models.sh ]; then
    echo "[MODEL] Installing LLaMA model weights..."
    bash llama_weights_and_models.sh
  fi

  # Copy Linux launcher
  if [ -f bootstrap/AscendAI.desktop ]; then
    cp bootstrap/AscendAI.desktop ./AscendAI.desktop
    chmod +x ./AscendAI.desktop
    echo "[LAUNCHER] AscendAI.desktop ready in project root."
  fi

  # ------- Devin installation -------
  if [ -f OpenDevin/install_devin.sh ]; then
    echo "[DEVIN] Installing OpenDevin..."
    bash OpenDevin/install_devin.sh
  else
    echo "[DEVIN] Warning: OpenDevin install script not found."
  fi

  echo "[INSTALL COMPLETE] You may now launch agents via ./bootstrap/launch_menu.sh or double-click AscendAI.desktop."

  read -p "Run Neo now? [Y/n]: " CONFIRM
  [[ "$CONFIRM" != "n" ]] && ./bootstrap/Neo.sh

# ----------- Windows / WSL -----------
else
  echo "[ENV] Windows detected (Git Bash, WSL, or similar)."

  if [ -f bootstrap/launch_matrix.bat ]; then
    cp bootstrap/launch_matrix.bat ./Launch_Ascend.bat
    echo "[LAUNCHER] Windows .bat launcher deployed."
  fi

  echo "[DEVIN] (Manual) Please run OpenDevin/install_devin.sh separately in Windows or WSL."

  echo "[INSTALL COMPLETE] Use Launch_Ascend.bat or run Neo via Git Bash."
fi
