#!/bin/zsh

# =====================[ CONDA ENV INSTALLER ]=====================

# Check for Conda
if ! command -v conda &> /dev/null; then
  echo "[-] Conda not found. Install Miniconda or Anaconda first."
  exit 1
fi

log_step() {
  echo "\n============================================="
  echo "[+] $1"
  echo "============================================="
}

create_env_base() {
  local name="$1"
  log_step "Resetting Conda env: $name"
  conda remove -n "$name" --all -y >/dev/null 2>&1 || true
  conda create -n "$name" python=3.10 -y || {
    echo "[!] Failed to create env: $name"; return 1
  }
}

install_cuda124_torchstack() {
  local name="$1"
  log_step "Installing CUDA 12.4 Torch in: $name"
  conda run -n "$name" pip install \
    torch==2.4.0+cu124 \
    torchvision==0.19.0+cu124 \
    torchaudio==2.4.0+cu124 \
    --index-url https://download.pytorch.org/whl/cu124 || {
      echo "[!] Torch install failed in: $name"; return 1
    }
}

install_pip_locked() {
  local name="$1"; shift
  log_step "Installing pip packages in: $name"
  conda run -n "$name" pip install --upgrade pip || true
  conda run -n "$name" pip install --no-deps "$@" || {
    echo "[!] Pip install failed in: $name"; return 1
  }
}

install_conda_forge() {
  local name="$1"; shift
  log_step "Installing conda-forge packages in: $name"
  conda install -n "$name" -c conda-forge "$@" -y || {
    echo "[!] Conda-forge install failed in: $name"; return 1
  }
}

# =====================[ ENV BUILD SEQUENCE ]=====================

# --- ai-core ---
create_env_base ai-core && \
install_cuda124_torchstack ai-core && \
install_pip_locked ai-core \
  transformers==4.40.1 \
  bitsandbytes==0.42.0 \
  accelerate==1.6.0 \
  xformers==0.0.30 \
  sentence-transformers==2.6.1 \
  pytorch-lightning==2.2.1 \
  optimum==1.19.1 \
  scipy==1.13.0 \
  numpy==1.26.4 || echo "[!] ai-core setup failed"

# =====================[ DONE ]=====================
log_step "✅ All Conda environments processed."

