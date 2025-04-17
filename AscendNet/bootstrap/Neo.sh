#!/bin/bash

echo "======================================"
echo "   [Neo] Initiating Boot Protocol..."
echo "======================================"

# Log the boot first
mkdir -p ascend_logs
echo "[BOOT] $(date)" >> ascend_logs/boot_timestamps.log

# Initialize task queue
mkdir -p task_queue
echo "Launch full matrix." > task_queue/init.task

# Make sure the Python core is executable
if [ ! -f AS_SK_C4.py ]; then
    echo "[ERROR] Sovereign kernel not found: AS_SK_C4.py"
    exit 1
fi

chmod +x AS_SK_C4.py

echo ">> [Neo] Launching Sovereign Kernel..."
./AS_SK_C4.py || { echo "[ERROR] Kernel launch failed."; exit 1; }

echo ">> [Neo] Launching Loop Engine & Supervisor..."
python3 Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py &
python3 Ascend_Infra/Supervision/ascend_supervisor_agent.py &

echo ">> [Neo] Systems online. Awaiting LLaMA ignition."