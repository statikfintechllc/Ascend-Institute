#!/bin/zsh

echo "[GremlinGPT] Creating conda environments..."
conda env create -f gremlin-nlp.yml
conda env create -f gremlin-dashboard.yml
conda env create -f gremlin-scraper.yml
conda env create -f gremlin-memory.yml
conda env create -f gremlin-orchestrator.yml
echo "[GremlinGPT] All environments created."

