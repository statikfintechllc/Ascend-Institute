#!/bin/bash
# Model Weights Download & Setup

mkdir -p ~/AscendAI/models/llama
cd ~/AscendAI/models/llama

# LLaMA 2 from Meta (manual download)
echo "Download LLaMA 2 from Meta official link after agreement:"
echo "https://ai.meta.com/resources/models-and-libraries/llama-downloads/"

# HuggingFace Access
# huggingface-cli login
# git lfs install
# git clone https://huggingface.co/meta-llama/Llama-2-7b-hf

mkdir -p ~/AscendAI/models/others
cd ~/AscendAI/models/others

# GPT4All
git clone https://github.com/nomic-ai/gpt4all
cd gpt4all
pip install -r requirements.txt
python download-model.py ggml-gpt4all-j-v1.3-groovy.bin

# Vicuna
git clone https://github.com/lm-sys/FastChat
cd FastChat
pip install -e .
python3 -m fastchat.model.download_model --model-name lmsys/vicuna-7b-v1.3

# Mistral 7B
git clone https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1

# Falcon
git clone https://huggingface.co/tiiuae/falcon-7b-instruct
