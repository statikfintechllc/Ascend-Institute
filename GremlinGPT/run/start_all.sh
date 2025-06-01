#!/bin/zsh

cd "$(dirname "$0")/.."
export GREMLIN_HOME="$PWD"
mkdir -p run/logs

# Set your preferred terminal emulator: gnome-terminal, xterm, or konsole
TERM_EMU=$(command -v gnome-terminal || command -v xterm)

function launch_terminal() {
  local title="$1"
  local env="$2"
  local cmd="$3"
  local logfile="$4"

  if command -v gnome-terminal > /dev/null; then
    gnome-terminal --title="$title" -- zsh -ic "
      echo '[${title}] Activating $env...';
      source ~/.zshrc;
      conda activate $env || { echo 'Failed to activate env: $env'; exit 1; };
      echo '[${title}] Running: $cmd';
      echo 'Output to: $logfile';
      $cmd | tee $logfile
      exec zsh
    "
  elif command -v xterm > /dev/null; then
    xterm -T "${title}" -e "
      source ~/.zshrc;
      conda activate $env || { echo 'Failed to activate env: $env'; exit 1; };
      echo '[${title}] Running: $cmd';
      $cmd | tee $logfile;
      exec zsh
    "
  else
    echo "No supported terminal emulator found (gnome-terminal or xterm)."
    exit 1
  fi
}

echo "[BOOT] Injecting GremlinGPT watermark to system trace."
echo "Boot ID: $(uuidgen) | Source: GremlinGPT | Time: $(date -u)" | tee -a run/logs/gremlin_boot_trace.log

echo "[START] Launching GremlinGPT subsystems in separate terminals..."

# NLP Service (if interactive, otherwise skip or set to background)
launch_terminal "NLP Service" gremlin-nlp "sleep infinity" "run/logs/nlp.out"

# Memory Service
launch_terminal "Memory Service" gremlin-memory "python memory/embedder.py" "run/logs/memory.out"

# Backend
launch_terminal "Backend Server" gremlin-dashboard "python backend/server.py" "run/logs/backend.out"

# FSM Agent
launch_terminal "FSM Agent" gremlin-orchestrator "python agent_core/fsm.py" "run/logs/fsm.out"

# Scraper
launch_terminal "Scraper" gremlin-scraper "python scraper/scraper_loop.py" "run/logs/scraper.out"

# Trainer
launch_terminal "Self-Trainer" gremlin-orchestrator "python self_training/trainer.py" "run/logs/trainer.out"

# Frontend Server (Python HTTP)
launch_terminal "Frontend" base "python3 -m http.server 8080 --directory frontend" "run/logs/frontend.out"

# Ngrok tunnel
launch_terminal "Ngrok Tunnel" base "python run/ngrok_launcher.py" "run/logs/ngrok.out"

echo "[ALL SYSTEMS LAUNCHED]"
echo "Backend:     http://localhost:8000  (see backend/server.py for port)"
echo "Frontend:    http://localhost:8080"
echo "Logs:        $GREMLIN_HOME/run/logs/"
