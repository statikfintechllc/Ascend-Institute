#!/bin/zsh

echo "[INSTALL] Initializing GremlinGPT installation..."

# Base structure
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

# Create placeholder metadata DB
touch memory/local_index/metadata.db
touch run/logs/runtime.log
touch run/checkpoints/state_snapshot.json
touch data/logs/bootstrap.log

# Setup environment
cd conda_envs && sudo chmod +x create_envs.sh && ./create_envs.sh && cd ..
echo "[*] Installing ngrok CLI (optional)..."
if ! command -v ngrok &> /dev/null; then
    echo "You may install it via: https://ngrok.com/download"
    echo "Or configure it via pyngrok in config.toml"
fi
echo "[INSTALL] GremlinGPT installed successfully."

