#!/bin/zsh

setopt NO_GLOB_SUBST

export PYTHONPATH="/home/statiksmoke8/SkylineX-AlphaWave/AscendAI/GremlinGPT"

cd "${0:a:h}/.."
export GREMLIN_HOME="$PWD"
mkdir -p run/logs

TERM_EMU=$(command -v gnome-terminal || command -v xterm)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

function launch_terminal() {
  local title="$1"
  local env="$2"
  local cmd="$3"
  local logfile="$4"

  local preamble="
    source \$HOME/miniconda3/etc/profile.d/conda.sh
    conda activate $env || { echo '[${title}] Failed to activate env: $env'; exec zsh; }
    echo '[${title}] ENV:' \$CONDA_DEFAULT_ENV
    echo '[${title}] CWD:' \$PWD
    echo '[${title}] Running: $cmd'
    $cmd | tee $logfile
    EXIT_CODE=\${PIPESTATUS[0]}
    echo '[${title}] Process exited with code' \$EXIT_CODE
    exec zsh
  "

  if command -v gnome-terminal > /dev/null; then
    gnome-terminal --title="$title" -- zsh --login -c "$preamble"
  elif command -v xterm > /dev/null; then
    xterm -T "$title" -e "zsh --login -c '$preamble'"
  else
    echo "No supported terminal emulator found (gnome-terminal or xterm)."
    exit 1
  fi
}

echo "[BOOT] Injecting GremlinGPT watermark to system trace."
echo "Boot ID: $(uuidgen) | Source: GremlinGPT | Time: $(date -u)" | tee -a run/logs/gremlin_boot_trace.log

echo "[START] Launching GremlinGPT subsystems in separate terminals..."

launch_terminal "Core Loop" gremlin-orchestrator "python core/loop.py" "run/logs/runtime.log"
launch_terminal "NLP Service" gremlin-nlp "python nlp_engine/nlp_check.py" "run/logs/nlp.out"
launch_terminal "Memory Service" gremlin-memory "python memory/vector_store/embedder.py" "run/logs/memory.out"
launch_terminal "Backend Server" gremlin-dashboard "python -m backend.server" "run/logs/backend.out"
launch_terminal "FSM Agent" gremlin-orchestrator "python -m agent_core.fsm" "run/logs/fsm.out"
launch_terminal "Scraper" gremlin-scraper "python -m scraper.scraper_loop" "run/logs/scraper.out"
launch_terminal "Self-Trainer" gremlin-nlp "python -m self_training.trainer" "run/logs/trainer.out"
launch_terminal "Frontend" gremlin-dashboard "python3 -m http.server 8080 --directory frontend" "run/logs/frontend.out"
launch_terminal "Ngrok Tunnel" gremlin-dashboard "python run/ngrok_launcher.py" "run/logs/ngrok.out"


echo "Backend:     http://localhost:8000  (see backend/server.py for port)"
echo "Frontend:    http://localhost:8080"
echo "Logs:        $GREMLIN_HOME/run/logs/"

