#!/bin/zsh

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

# Spinner Function
spin() {
    local -a marks=('|' '/' '-' '\\')
    local pid=$!
    local i=0
    while kill -0 $pid 2>/dev/null; do
        printf "\r${RED}GremlinGPT${NC} initializing ${marks[i++ % 4]}"
        sleep 0.1
    done
    printf "\r${RED}GremlinGPT${NC} initialized ✅\n"
}

echo "[INSTALL] Initializing GremlinGPT installation..."

# Step 1: Create Required Directory Structure
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
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    echo "Created: $dir"
  else
    echo "Exists:  $dir"
  fi
done

# Step 2: Create Metadata / Log Files
echo "[*] Creating placeholder metadata/log files if missing..."
touch memory/local_index/metadata.db
touch run/logs/runtime.log
touch run/checkpoints/state_snapshot.json
touch data/logs/bootstrap.log

# Step 3: Ensure Conda is in path and initialized
echo "[*] Checking conda..."
if ! command -v conda &> /dev/null; then
    echo "[INFO] Attempting to source conda..."
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
        echo "[ERROR] Conda not found. Please install or check your path."
        exit 1
    fi
fi

# Step 4: Build Conda Environments
echo "[*] Creating conda environments if they don't exist..."
(
  cd conda_envs || exit 1

  # Add check for whether environments already exist inside create_envs.sh
  chmod +x create_envs.sh && ./create_envs.sh
) & spin

# Step 5: Download NLP Models (if not already downloaded)
echo "[*] Downloading required NLP models..."

(
  ENV_NAME="gremlin-nlp"

  if ! conda info --envs | grep -q "$ENV_NAME"; then
      echo "[ERROR] Environment '$ENV_NAME' does not exist. Cannot download models."
      exit 1
  fi

  source "$HOME/miniconda3/etc/profile.d/conda.sh"
  conda activate "$ENV_NAME" || exit 1

  CACHE_PATH="$HOME/.cache/huggingface/transformers"

  if [ ! -d "$CACHE_PATH/models--bert-base-uncased" ]; then
      echo "Downloading: BERT base uncased"
      python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')" || exit 1
  else
      echo "Model already cached: BERT base uncased"
  fi

  if [ ! -d "$CACHE_PATH/sentence-transformers--all-MiniLM-L6-v2" ]; then
      echo "Downloading: SentenceTransformer MiniLM"
      python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" || exit 1
  else
      echo "Model already cached: SentenceTransformer MiniLM"
  fi

  conda deactivate
) & spin

# Step 6: ngrok (optional)
echo "[*] Checking for ngrok CLI..."
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi

# Final message
echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"

