#!/bin/bash

# PRELOAD
PASS_MODULES=()
FAIL_MODULES=()

log_pass() {
  PASS_MODULES+=("$1")
}

log_fail() {
  FAIL_MODULES+=("$1")
}

check() {
  DESC="$1"
  CMD="$2"
  echo "--- $DESC ---"
  if python3 -c "$CMD" &>/dev/null; then
    log_pass "$DESC"
    echo "✓ $DESC loaded"
  else
    log_fail "$DESC"
    echo "✗ $DESC failed"
  fi
}

echo "===[ GREMLIN SYSTEM BOOT TEST ]==="
echo "[1/6] Activating environments..."

conda activate gremlin-nlp && echo "✓ NLP env ready"
conda activate gremlin-memory && echo "✓ Memory env ready"
conda activate gremlin-scraper && echo "✓ Scraper env ready"
conda activate gremlin-dashboard && echo "✓ Dashboard env ready"
conda activate gremlin-orchestrator && echo "✓ Orchestrator env ready"

echo "[2/6] Running module health checks..."

check "NLP Core" "from nlp_engine import tokenizer, transformer_core, semantic_score"
check "Memory Embedder" "from memory.vector_store import embedder"
check "Agent FSM" "from agent_core import fsm, task_queue"
check "Self-Training" "from self_training import trainer, mutation_engine"
check "Scraper Loop" "from scraper import scraper_loop, dom_navigator"
check "Backend Core" "from backend import server, router, state_manager"

echo "[3/6] Checking log file write access..."
if touch run/logs/runtime.log &>/dev/null; then
  log_pass "Log File Write"
  echo "✓ Log file writable"
else
  log_fail "Log File Write"
  echo "✗ Cannot write to log file"
fi

echo "[4/6] Snapshot read/write check..."
if echo '{}' > run/checkpoints/test_snapshot.json; then
  log_pass "Checkpoint Write"
  echo "✓ Checkpoint write OK"
else
  log_fail "Checkpoint Write"
  echo "✗ Failed to write checkpoint"
fi

echo "[6/6] Summary Output"
echo ""

python3 - <<EOF
from rich.table import Table
from rich.console import Console

passed = ${#PASS_MODULES[@]}
failed = ${#FAIL_MODULES[@]}

table = Table(title="GremlinGPT System Test Summary")
table.add_column("Module", style="cyan", no_wrap=True)
table.add_column("Status", style="green")

for mod in ${PASS_MODULES[@]}; do
    table.add_row("$mod", "[bold green]PASS[/bold green]")
done

for mod in ${FAIL_MODULES[@]}; do
    table.add_row("$mod", "[bold red]FAIL[/bold red]")
done

console = Console()
console.print(table)

if $failed -eq 0:
    console.print("\n[bold green]All systems go. You may now run start_all.sh[/bold green]")
else:
    console.print(f"\n[bold red]{failed} module(s) failed.[/bold red] Please check logs.")
EOF
