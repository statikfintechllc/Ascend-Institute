#!/bin/bash

echo "=============================="
echo "  ASCEND MATRIX INITIALIZER"
echo "=============================="
echo ">> Checking system integrity..."

# Ensure Neo is executable
if [ ! -f Neo.sh ]; then
  echo "[ERROR] Neo.sh not found in current directory."
  exit 1
fi

chmod +x Neo.sh

echo ">> Launching Sovereign Core..."
./Neo.sh || { echo "[ERROR] Neo.sh execution failed."; exit 1; }