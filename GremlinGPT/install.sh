#!/bin/zsh

# Colors
RED='\033[1;31m'
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
  mkdir -p "$dir"
done

# Step 2: Create Metadata / Log Files
touch memory/local_index/metadata.db
touch run/logs/runtime.log
touch run/checkpoints/state_snapshot.json
touch data/logs/bootstrap.log

# Step 3: Build Conda Environments (with spinner)
(
  cd conda_envs || exit 1
  chmod +x create_envs.sh && ./create_envs.sh || exit 1
) & spin

# Step 4: Source Conda If Needed
if ! command -v conda &> /dev/null; then
    source ~/miniconda3/etc/profile.d/conda.sh
fi

# Step 5: Download NLP Models (with spinner)
(
  conda activate gremlin-nlp || exit 1
  python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('bert-base-uncased'); AutoModel.from_pretrained('bert-base-uncased')" || exit 1
  python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" || exit 1
  conda deactivate
) & spin

# Step 6: ngrok Info Message
echo "[*] Installing ngrok CLI (optional)..."
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
fi

# Final Message
echo "[INSTALL] GremlinGPT installation completed successfully."
