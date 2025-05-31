#!/bin/zsh

set -e

# --- UNIVERSAL NETCAT INSTALL ---
if ! command -v nc &>/dev/null; then
    echo "[INFO] netcat (nc) not found. Installing..."
    if [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y netcat
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y nc
    elif [ -f /etc/arch-release ]; then
        sudo pacman -Sy --noconfirm gnu-netcat
    else
        echo "ERROR: Cannot auto-install netcat. Please install manually."
        exit 1
    fi
fi

# Determine project root (script can be run from anywhere)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Go to project root if run from run/
if [[ "$(basename "$PWD")" == "run" ]]; then
  cd ..
fi

PROJECT_ROOT="$PWD"

echo "===[ GREMLIN SYSTEM BOOT TEST ]==="

# Auto-detect conda base
if [[ -z "$CONDA_EXE" ]]; then
    if [ -x "$HOME/miniconda3/bin/conda" ]; then
        CONDA_BIN="$HOME/miniconda3/bin/conda"
    elif [ -x "$HOME/anaconda3/bin/conda" ]; then
        CONDA_BIN="$HOME/anaconda3/bin/conda"
    else
        CONDA_BIN=$(which conda)
    fi
else
    CONDA_BIN="$CONDA_EXE"
fi

if [[ ! -x "$CONDA_BIN" ]]; then
    echo "ERROR: Conda not found! Aborting."
    exit 1
fi

eval "$($CONDA_BIN shell.bash hook 2> /dev/null)"

PASS_MODULES=()
FAIL_MODULES=()

log_pass() { PASS_MODULES+=("$1"); }
log_fail() { FAIL_MODULES+=("$1"); }

check_env() {
    ENV="$1"
    DESC="$2"
    CMD="$3"

    echo "--- $DESC [$ENV] ---"
    conda activate "$ENV"
    if python3 -c "$CMD" &>/dev/null; then
        log_pass "$DESC"
        echo "✓ $DESC loaded"
    else
        log_fail "$DESC"
        echo "✗ $DESC failed"
    fi
    conda deactivate
}

# [1/6] ENV BOOT
echo "[1/6] Running module health checks in dedicated environments..."

check_env "gremlin-nlp"         "NLP Core"           "from nlp_engine import tokenizer, transformer_core, semantic_score"
check_env "gremlin-memory"      "Memory Embedder"    "from memory.vector_store import embedder"
check_env "gremlin-orchestrator" "Agent FSM"         "from agent_core import fsm, task_queue"
check_env "gremlin-orchestrator" "Self-Training"     "from self_training import trainer, mutation_engine"
check_env "gremlin-scraper"     "Scraper Loop"       "from scraper import scraper_loop, dom_navigator"
check_env "gremlin-dashboard"   "Backend Core"       "from backend import server, router, state_manager"

# [2/6] LOG FILES
echo "[2/6] Checking log file write access..."
mkdir -p run/logs
if touch run/logs/runtime.log &>/dev/null; then
  log_pass "Log File Write"
  echo "✓ Log file writable"
else
  log_fail "Log File Write"
  echo "✗ Cannot write to log file"
fi

# [3/6] CHECKPOINT FILE
echo "[3/6] Snapshot read/write check..."
mkdir -p run/checkpoints
if echo '{}' > run/checkpoints/test_snapshot.json; then
  log_pass "Checkpoint Write"
  echo "✓ Checkpoint write OK"
else
  log_fail "Checkpoint Write"
  echo "✗ Failed to write checkpoint"
fi

# [4/6] CODE WATCHER
echo "[4/6] Code watcher dry run (gremlin-orchestrator)..."
conda activate gremlin-orchestrator
if python3 self_mutation_watcher/watcher.py --dry-run &>/dev/null; then
  log_pass "Watcher"
  echo "✓ Watcher executed"
else
  log_fail "Watcher"
  echo "✗ Watcher failed"
fi
conda deactivate

# [5/6] BACKEND PORT TEST (8000)
echo "[5/6] Backend port check (8000)..."
conda activate gremlin-dashboard
python backend/server.py > /dev/null 2>&1 &
PID=$!
sleep 3
# Set this port to the real port your backend uses (edit if needed)
BACKEND_PORT=8000
if nc -z localhost $BACKEND_PORT; then
  log_pass "Backend Port $BACKEND_PORT"
  echo "✓ Backend port $BACKEND_PORT is open"
else
  log_fail "Backend Port $BACKEND_PORT"
  echo "✗ Backend port $BACKEND_PORT is not responding"
fi
kill $PID
conda deactivate

# [6/6] SUMMARY
echo ""
echo "-------------------------------"
echo "GremlinGPT System Test Summary"
echo "-------------------------------"

for mod in "${PASS_MODULES[@]}"; do
    echo -e "✓ $mod"
done

for mod in "${FAIL_MODULES[@]}"; do
    echo -e "✗ $mod"
done

if [ ${#FAIL_MODULES[@]} -eq 0 ]; then
    echo -e "\n✅ All systems go. You may now run ./run/start_all.sh"
    exit 0
else
    echo -e "\n⚠️  ${#FAIL_MODULES[@]} module(s) failed. Please check logs."
    exit 1
fi
