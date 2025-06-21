#!/bin/zsh

setopt NO_GLOB_SUBST
set -u
set -o pipefail

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
  "nltk_data"
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


# 3. Conda init
echo "[*] Ensuring conda is initialized..."
if ! command -v conda &> /dev/null; then
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    fi
fi
eval "$(conda shell.zsh hook 2>/dev/null)" || eval "$(conda shell.bash hook 2>/dev/null)"

# 4. Build all conda environments
echo "[*] Building all conda environments via ./conda_envs/create_envs.sh..."
if [ -f "./conda_envs/create_envs.sh" ]; then
    chmod +x ./conda_envs/create_envs.sh
    ./conda_envs/create_envs.sh || { echo "${RED}[ERROR] Failed creating envs${NC}"; exit 1; }
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


function pip_install_or_fail {
  pip install --upgrade pip || { echo '${RED}[FAIL] pip upgrade${NC}'; exit 1; }
  for pkg in "$@"; do
    pip install "$pkg" || { echo "${RED}[FAIL] pip install $pkg${NC}"; exit 1; }
  done
}


function download_nltk {
  python3 -m nltk.downloader --dir=/user/share/data/nltk_data punkt averaged_perceptron_tagger wordnet stopwords || \
  { echo "${RED}[FAIL] NLTK data download${NC}"; exit 1; }
}

# 5. gremlin-nlp env setup
echo "[*] Activating gremlin-nlp and installing deps..."
conda activate gremlin-nlp
pip_install_or_fail spacy torch torchvision torchaudio sentence-transformers transformers bs4 nltk pytesseract playwright pyautogui
python -m spacy download en_core_web_sm || { echo "${RED}[FAIL] spaCy model${NC}"; exit 1; }
playwright install || { echo "${RED}[FAIL] playwright${NC}"; exit 1; }
pip install nltk  # or pip_install_or_fail ... as in your script
python -m nltk.downloader -d ./nltk_data punkt
download_nltk
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
conda deactivate

# 6. gremlin-scraper env setup
echo "[*] Activating gremlin-scraper..."
conda activate gremlin-scraper
pip_install_or_fail torch torchvision torchaudio sentence-transformers transformers playwright pyautogui
python -m spacy download en_core_web_sm
playwright install
check_cuda
conda deactivate

# 7. gremlin-dashboard env setup
echo "[*] Activating gremlin-dashboard..."
conda activate gremlin-dashboard
pip_install_or_fail torch torchvision torchaudio sentence-transformers transformers pyautogui
check_cuda
conda deactivate

# 8. gremlin-orchestrator env setup
echo "[*] Activating gremlin-orchestrator..."
conda activate gremlin-orchestrator
pip_install_or_fail torch torchvision torchaudio backend bs4 nltk langdetect pytesseract sentence-transformers transformers playwright pyautogui
python -m spacy download en_core_web_sm
playwright install
pip install nltk  # or pip_install_or_fail ... as in your script
python -m nltk.downloader -d ./nltk_data punkt
download_nltk
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
conda deactivate

# 9. ngrok CLI check
echo "[*] Checking for ngrok CLI..."
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi


REPO="$(cd "$(dirname "$0")/.." && pwd)"
APPDIR="$HOME/.local/share/applications"
ICNDIR="$HOME/.local/share/icons"

mkdir -p "$APPDIR" "$ICNDIR"

mkdir -p "$ICNDIR"

cp "$REPO/GremlinGPT/frontend/Icon_Logo/App_Icon_&_Loading_&_Inference_Image.png" "$ICNDIR/AscendAI-v1.0.3.png"

cat > "$APPDIR/AscendAI-v1.0.3.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=AscendAI-v1.0.3
Comment=SFTi
Exec=$HOME/AscendAI/GremlinGPT/run/start_all.sh
Icon=$ICNDIR/AscendAI-v1.0.3.png
Terminal=true
Categories=Development;Utility;
EOF

echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"
