#!/bin/zsh

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
  whisper-agent
  stealth-core
  surveillance-stack
  telemetry-ops
  vector-db
  webui
)

for env in $envs; do
  echo "\n============================================="
  echo "[📦] PACKAGES FOR ENV: $env"
  echo "============================================="
  conda list -n "$env" 2>/dev/null || echo "[!] Failed to load env: $env"
done
