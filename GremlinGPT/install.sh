#!/bin/zsh

# Output colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${GREEN}[INSTALL] Initializing GremlinGPT installation...${NC}"

# 1. Directory structure
echo "[*] Creating directory structure..."
DIRS=(
  "run/logs"
  "run/checkpoints"
  "data/prompts"
  "data/raw_scrapes"
  "data/embeddings"
  "data/nlp_training_sets"
  "data/logs"
  "memory/vector_store/faiss"
  "memory/vector_store/chroma"
  "memory/local_index/documents"
  "memory/local_index/scripts"
  "scraper/persistence/cookies"
  "scraper/profiles/chromium_profile"
  "frontend/components"
  "tests"
  "docs"
)
for dir in "${DIRS[@]}"; do
  [ ! -d "$dir" ] && mkdir -p "$dir" && echo "Created: $dir" || echo "Exists:  $dir"
done

# 2. Placeholder files
echo "[*] Creating placeholder metadata/log files if missing..."
touch memory/local_index/metadata.db
touch run/logs/runtime.log
touch run/checkpoints/state_snapshot.json
touch data/logs/bootstrap.log

# 3. Conda init (NO 'set -e', NO error exit)
echo "[*] Ensuring conda is initialized..."
if ! command -v conda &> /dev/null; then
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    fi
fi

eval "$(conda shell.zsh hook 2>/dev/null)" || eval "$(conda shell.bash hook 2>/dev/null)"

# 4. Run create_envs.sh (NO extra error traps)
echo "[*] Building all conda environments via ./conda_envs/create_envs.sh..."
if [ -f "./conda_envs/create_envs.sh" ]; then
    chmod +x ./conda_envs/create_envs.sh
    ./conda_envs/create_envs.sh
else
    echo "${RED}[ERROR] ./conda_envs/create_envs.sh not found!${NC}"
fi

# 5. Activate gremlin-nlp for HuggingFace models
echo "[*] Activating gremlin-nlp to download HuggingFace models..."
conda activate gremlin-nlp
CACHE_PATH="$HOME/.cache/huggingface/transformers"
if [ ! -d "$CACHE_PATH/models--bert-base-uncased" ]; then
    echo "[MODEL] Downloading: BERT base uncased"
    python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')"
else
    echo "[MODEL] Already cached: BERT base uncased"
fi
if [ ! -d "$CACHE_PATH/sentence-transformers--all-MiniLM-L6-v2" ]; then
    echo "[MODEL] Downloading: SentenceTransformer MiniLM"
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', device='cpu')"
else
    echo "[MODEL] Already cached: SentenceTransformer MiniLM"
fi
pip install playwright
playwright install
conda deactivate

# 6. Activate gremlin-scraper for Playwright install
echo "[*] Activating gremlin-scraper to install Playwright browsers..."
conda activate gremlin-scraper
pip install playwright
playwright install
conda deactivate

echo "[*] Activating gremlin-scraper to install Playwright browsers..."
conda activate gremlin-orchestrator
pip install playwright
playwright install
conda deactivate

# 7. ngrok CLI check
echo "[*] Checking for ngrok CLI..."
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi

echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"
