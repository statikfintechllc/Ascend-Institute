#!/bin/zsh

echo "[GremlinGPT] Creating conda environments..."

# List of environment names and their corresponding YAML files
ENV_FILES=(
  "gremlin-nlp:gremlin-nlp.yml"
  "gremlin-dashboard:gremlin-dashboard.yml"
  "gremlin-scraper:gremlin-scraper.yml"
  "gremlin-memory:gremlin-memory.yml"
  "gremlin-orchestrator:gremlin-orchestrator.yml"
)

# Loop through each environment and create it if it doesn't exist
for item in "${ENV_FILES[@]}"; do
  ENV_NAME="${item%%:*}"
  YAML_FILE="${item##*:}"

  echo "[INFO] Checking environment: $ENV_NAME"

  # Check if env exists
  if conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "[SKIP] Environment '$ENV_NAME' already exists."
    continue
  fi

  # Check if YAML file exists
  if [ ! -f "$YAML_FILE" ]; then
    echo "[ERROR] YAML file '$YAML_FILE' not found. Skipping environment '$ENV_NAME'."
    continue
  fi

  # Create environment
  echo "[CREATE] Creating '$ENV_NAME' from '$YAML_FILE'..."
  conda env create -f "$YAML_FILE"
  if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create environment: $ENV_NAME"
    exit 1
  fi
done

echo "[GremlinGPT] ✅ All environments checked and created if necessary."
