#!/bin/zsh

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

function check_cuda {
  echo "[*] Checking CUDA in current environment:"
  python -c "
import torch
print('[CUDA] torch.cuda.is_available:', torch.cuda.is_available())
print('[CUDA] torch.cuda.device_count:', torch.cuda.device_count())
print('[CUDA] torch.cuda.current_device:', torch.cuda.current_device() if torch.cuda.is_available() else None)
print('[CUDA] torch.cuda.get_device_name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
" || echo "${RED}[CUDA] PyTorch not installed or failed.${NC}"
}

# 5. Activate gremlin-nlp, install GPU deps, download models, check CUDA
echo "[*] Activating gremlin-nlp to download HuggingFace models and set up CUDA..."
conda activate gremlin-nlp
pip install --upgrade pip
python -m spacy download en_core_web_sm
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install sentence-transformers transformers
pip install bs4 nltk pytesseract playwright
playwright install
python -m spacy download en_core_web_sm
pyautogui
check_cuda

# Download core models to GPU cache (test both BERT and MiniLM for CUDA)
python -c "
from transformers import AutoTokenizer, AutoModel
import torch
print('[GPU-TEST] Loading BERT on', 'cuda' if torch.cuda.is_available() else 'cpu')
AutoTokenizer.from_pretrained('bert-base-uncased')
AutoModel.from_pretrained('bert-base-uncased').to('cuda' if torch.cuda.is_available() else 'cpu')
"
python -c "
from sentence_transformers import SentenceTransformer
import torch
print('[GPU-TEST] Loading MiniLM on', 'cuda' if torch.cuda.is_available() else 'cpu')
SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')
"
conda deactivate

# 6. Activate gremlin-scraper
echo "[*] Activating gremlin-scraper for Playwright install and CUDA test..."
conda activate gremlin-scraper
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install sentence-transformers transformers playwright
playwright install
python -m spacy download en_core_web_sm
check_cuda
conda deactivate

# 7. Activate gremlin-dashboard for transformers/sentence_transformers
echo "[*] Activating gremlin-dashboard for dashboard deps and CUDA test..."
conda activate gremlin-dashboard
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install sentence-transformers transformers
check_cuda
conda deactivate

# 8. Activate gremlin-orchestrator for all deps and CUDA test...
echo "[*] Activating gremlin-orchestrator for all deps and CUDA test..."
conda activate gremlin-orchestrator
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install backend bs4 nltk langdetect pytesseract sentence-transformers transformers
python -m spacy download en_core_web_sm
check_cuda
python -c "
from transformers import AutoTokenizer, AutoModel
import torch
print('[GPU-TEST] Loading BERT on', 'cuda' if torch.cuda.is_available() else 'cpu')
AutoTokenizer.from_pretrained('bert-base-uncased')
AutoModel.from_pretrained('bert-base-uncased').to('cuda' if torch.cuda.is_available() else 'cpu')
"
python -c "
from sentence_transformers import SentenceTransformer
import torch
print('[GPU-TEST] Loading MiniLM on', 'cuda' if torch.cuda.is_available() else 'cpu')
SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')
"
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install playwright
playwright install
check_cuda
conda deactivate

# 9. ngrok CLI check
echo "[*] Checking for ngrok CLI..."
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi

echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"
