#!/bin/zsh

# Output directory for environment package listings
OUTDIR="$HOME/gremlin_env_reports"
mkdir -p "$OUTDIR"

# List of known environments (explicit, from your output)
envs=(
  base
  ai-agents
  ai-core
  ai-eval
  base-dev
  code-fuzz
  darknet-interface
  dashboard-ui
  finops
  intel-recon
  ml-ops-deploy
  nanogpt-wrapper
  netsec-tools
  opendevin
  quantum-research
  runmistral
  starcoder-wrapper
  stealth-core
  surveillance-stack
  telemetry-ops
  vector-db
  webui
)

echo "[+] Logging installed packages for all environments..."

for env in $envs; do
  echo "[>] $env"
  conda list -n "$env" > "$OUTDIR/${env}_packages.txt" 2>/dev/null || echo "[!] Failed: $env"
done

echo "[✓] Package logs saved to: $OUTDIR"
