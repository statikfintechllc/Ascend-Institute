#!/usr/bin/env zsh

# Only set zsh-specific options if running under zsh
if [ -n "$ZSH_VERSION" ]; then
  setopt NO_GLOB_SUBST
fi
set -u
# Only set pipefail if supported (bash or zsh)
if [ -n "$BASH_VERSION" ] || [ -n "$ZSH_VERSION" ]; then
  set -o pipefail
fi

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${GREEN}[INSTALL] Initializing GremlinGPT installation...${NC}"

REPO="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
APPDIR="$HOME/.local/share/applications"
APPLOC="$HOME/AscendAI/GremlinGPT"
ICNDIR="$HOME/.local/share/icons"

if [ ! -d "$APPLOC" ]; then
    mkdir -p "$APPLOC"
    echo "[*] Created application directory: $APPLOC"
else
    echo "[*] Application directory already exists: $APPLOC"
fi

mkdir -p "$APPDIR" "$ICNDIR"

ICON_SRC="$REPO/GremlinGPT/frontend/Icon_Logo/App_Icon_&_Loading_&_Inference_Image.png"
if [ -f "$ICON_SRC" ]; then
  cp "$ICON_SRC" "$ICNDIR/AscendAI-v1.0.3.png"
else
  echo "${YELLOW}[WARNING] Icon file not found at $ICON_SRC. Skipping icon copy.${NC}"
fi

DASH_CLI_PATH="$APPLOC/utils/dash_cli.sh"
cat > "$APPDIR/AscendAI-v1.0.3.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=AscendAI-v1.0.3
Comment=SFTi
Exec=$DASH_CLI_PATH
Icon=$ICNDIR/AscendAI-v1.0.3.png
Terminal=true
Categories=Development;Utility;
EOF

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
  "data/nltk_data"
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

echo "[*] Ensuring conda is initialized..."
if ! eval "$(conda shell.zsh hook 2>/dev/null)"; then
    if ! eval "$(conda shell.bash hook 2>/dev/null)"; then
        # Fallback: source conda.sh directly if hooks fail
        if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
            source "$HOME/miniconda3/etc/profile.d/conda.sh"
        else
            echo "${RED}[ERROR] Could not initialize conda environment.${NC}"
            exit 1
        fi
    fi
fi
eval "$(conda shell.zsh hook 2>/dev/null)" || eval "$(conda shell.bash hook 2>/dev/null)"
        echo "${RED}[ERROR] Could not initialize conda environment.${NC}"
        exit 1
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
check_cuda() {
  echo "[*] Checking CUDA in current environment:"
  python -c "
import torch
print('[CUDA] torch.cuda.is_available:', torch.cuda.is_available())
print('[CUDA] torch.cuda.device_count:', torch.cuda.device_count())
print('[CUDA] torch.cuda.current_device:', torch.cuda.current_device() if torch.cuda.is_available() else None)
print('[CUDA] torch.cuda.get_device_name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
" || echo "${RED}[CUDA] PyTorch not installed or failed.${NC}"
}

pip_install_or_fail() {
  pip install --upgrade pip || { echo '${RED}[FAIL] pip upgrade${NC}'; exit 1; }
  for pkg in "$@"; do
    pip install "$pkg" || { echo "${RED}[FAIL] pip install $pkg${NC}"; exit 1; }
  done
}

download_nltk() {
  export NLTK_DATA=./data/nltk_data
  python3 -m nltk.downloader --dir="$NLTK_DATA" punkt averaged_perceptron_tagger wordnet stopwords || \
  { echo "${RED}[FAIL] NLTK data download${NC}"; exit 1; }
}
  { echo "${RED}[FAIL] NLTK data download${NC}"; exit 1; }
}

# 5. gremlin-nlp env setup
echo "[*] Activating gremlin-nlp and installing deps..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-nlp
pip_install_or_fail spacy torch torchvision torchaudio sentence-transformers transformers bs4 nltk pytesseract playwright pyautogui
python -m spacy download en_core_web_sm || { echo "${RED}[FAIL] spaCy model${NC}"; exit 1; }
playwright install || { echo "${RED}[FAIL] playwright${NC}"; exit 1; }
pip install nltk
export NLTK_DATA=./data/nltk_data
python -m nltk.downloader -d "$NLTK_DATA" punkt
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
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-scraper
pip_install_or_fail torch torchvision torchaudio sentence-transformers transformers playwright pyautogui
python -m spacy download en_core_web_sm
playwright install
check_cuda
conda deactivate

# 7. gremlin-dashboard env setup
echo "[*] Activating gremlin-dashboard..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-dashboard
pip_install_or_fail torch torchvision torchaudio sentence-transformers transformers pyautogui
check_cuda
conda deactivate

# 8. gremlin-orchestrator env setup
echo "[*] Activating gremlin-orchestrator..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-orchestrator
pip_install_or_fail torch torchvision torchaudio backend bs4 nltk langdetect pytesseract sentence-transformers transformers playwright pyautogui
python -m spacy download en_core_web_sm
playwright install
pip install nltk
export NLTK_DATA=./data/nltk_data
python -m nltk.downloader -d "$NLTK_DATA" punkt
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
    echo "${YELLOW}[NOTICE] ngrok not found.${NC}"
    echo "You can install ngrok by following the instructions at: https://ngrok.com/download"
    read -r -p "Would you like to attempt automatic installation of ngrok? (y/N): " install_ngrok
    if [[ "$install_ngrok" =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            wget -O ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip && \
            unzip ngrok.zip -d "$HOME/.local/bin" && \
            chmod +x "$HOME/.local/bin/ngrok" && \
            rm ngrok.zip && \
            echo "${GREEN}[INFO] ngrok installed to $HOME/.local/bin/ngrok${NC}" || \
            echo "${RED}[ERROR] Failed to install ngrok automatically.${NC}"
            export PATH="$HOME/.local/bin:$PATH"
            # Instruct user to persist PATH for future shells
            SHELL_PROFILE=""
            if [ -n "$ZSH_VERSION" ]; then
              SHELL_PROFILE="$HOME/.zshrc"
            elif [ -n "$BASH_VERSION" ]; then
              SHELL_PROFILE="$HOME/.bashrc"
            else
              SHELL_PROFILE="$HOME/.profile"
            fi
            if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_PROFILE"; then
              echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_PROFILE"
              echo "${YELLOW}[NOTICE] Added ngrok path to $SHELL_PROFILE. Restart your terminal or run: source $SHELL_PROFILE${NC}"
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install ngrok || echo "${RED}[ERROR] Failed to install ngrok via Homebrew.${NC}"
        else
            echo "${YELLOW}[NOTICE] Please install ngrok manually for your OS.${NC}"
        fi
    else
        echo "${YELLOW}[NOTICE] Skipping ngrok installation. You can install it later from https://ngrok.com/download${NC}"
    fi
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi

# ─────────────────────────────────────────────────────────────

sudo apt install xdotool util-linux

# 10. Setup systemd service
echo "[*] Setting up systemd service..."

SYSTEMD_UNIT_PATH="/etc/systemd/system/gremlin.service"
START_SCRIPT="$APPLOC/start_all.sh"

sudo tee "$SYSTEMD_UNIT_PATH" > /dev/null <<EOF
[Unit]
Description=GremlinGPT Autonomous Agent
After=network.target

[Service]
Type=simple
WorkingDirectory=$APPLOC
ExecStart=/bin/zsh -c 'conda activate gremlin-orchestrator && $START_SCRIPT'
Restart=always
RestartSec=10
User=$USER
Environment="PATH=$HOME/miniconda3/envs/gremlin-orchestrator/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable gremlin.service
sudo systemctl restart gremlin.service

echo "[✓] Systemd service registered and running."

# ─────────────────────────────────────────────────────────────
# 11. Setup RTC wake & login filler from config
echo "[*] Setting RTC wake + GUI login automation..."

WAKE_SCRIPT="/usr/local/bin/set-wake-timer.sh"
LOGIN_SCRIPT="$APPLOC/utils/tws_stt_autologin.sh"
CONFIG_PATH="$APPLOC/config/config.toml"

sudo tee "$WAKE_SCRIPT" > /dev/null <<EOF
#!/bin/zsh
rtcwake -m no -t \$(date -d 'tomorrow 03:30' +%s)
EOF
sudo chmod +x "$WAKE_SCRIPT"
(crontab -l 2>/dev/null; echo "@reboot $WAKE_SCRIPT") | crontab -

# 12. Pulling login creds from config.toml
TWS_USER=$(grep -oP '(?<=tws_username\s?=\s?")[^"]*' "$CONFIG_PATH")
TWS_PASS=$(grep -oP '(?<=tws_password\s?=\s?")[^"]*' "$CONFIG_PATH")
STT_USER=$(grep -oP '(?<=stt_username\s?=\s?")[^"]*' "$CONFIG_PATH")
STT_PASS=$(grep -oP '(?<=stt_password\s?=\s?")[^"]*' "$CONFIG_PATH")

mkdir -p "$APPLOC/utils"
tee "$LOGIN_SCRIPT" > /dev/null <<EOF
#!/bin/zsh
sleep 20

# TWS Auto-login
xdotool search --name "Trader Workstation" windowactivate --sync \
  key Tab key Tab type '$TWS_USER' key Tab \
  type '$TWS_PASS' key Return

# STT Auto-login
xdotool search --name "StocksToTrade" windowactivate --sync \
  key Tab type '$STT_USER' key Tab \
  type '$STT_PASS' key Return
EOF

chmod +x "$LOGIN_SCRIPT"

# Optional autostart (user-controlled)
echo "@reboot $LOGIN_SCRIPT" | crontab -

echo "${GREEN}[✓] Wake timer, autologin, and systemd service bootstrapped.${NC}"

# 13. Finalize installation
echo "[*] Finalizing installation..."
echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"
echo "[*] Installation complete! You can now run GremlinGPT using the desktop entry or via the command line."
