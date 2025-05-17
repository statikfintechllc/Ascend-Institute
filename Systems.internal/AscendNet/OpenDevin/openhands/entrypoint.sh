#!/bin/bash

# Add micromamba to PATH
export PATH="/openhands/micromamba/bin:$PATH"

# Init shell support
eval "$(micromamba shell hook --shell=bash)"

# Activate the openhands conda env
micromamba activate openhands

# Move into root source dir (where pyproject.toml and openhands/ folder are)
cd /OpenDevin

# Launch app
exec poetry run python -m openhands.main
