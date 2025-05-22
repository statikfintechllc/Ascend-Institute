#!/bin/bash

# AscendNet AI Stack Installer
# Folder: SkylineX
# Env: AscendAI

set -e

# Define working directory and venv
BASE_DIR="$HOME/SkylineX"
VENV_DIR="$BASE_DIR/AscendAI"

echo ">> Creating project directory at $BASE_DIR"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

# Create and activate virtual environment
echo ">> Creating virtual environment in $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo ">> Upgrading pip"
pip install --upgrade pip

# Install Python packages
echo ">> Installing base dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install accelerate transformers bitsandbytes sentencepiece datasets \
            gradio fastapi uvicorn llama-index langchain streamlit \
            chromadb faiss-cpu openai pydantic tiktoken \
            rich watchdog pyngrok typer debugpy huggingface_hub gdown aiohttp websockets

# Clone key components
echo ">> Cloning core agent repositories..."
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make -j$(nproc) && cd ..

git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui && pip install -r requirements.txt && cd ..

git clone https://github.com/Torantulino/Auto-GPT.git
cd Auto-GPT && pip install -r requirements.txt && cd ..

git clone https://github.com/yoheinakajima/babyagi.git
cd babyagi && pip install -r requirements.txt && cd ..

git clone https://github.com/bigcode-project/starcoder.git
cd starcoder && pip install -r requirements.txt && cd ..

echo ">> Installation complete. Run './run_ascendnet.sh' from $BASE_DIR to unleash the machine."