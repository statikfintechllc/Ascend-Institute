#!/bin/bash

echo ">> [Neo] Initiating boot protocol..."

# Make sure the Python launcher is executable and launch it
chmod +x AS_SK_C4.py
./AS_SK_C4.py

# Log the boot
mkdir -p ascend_logs
echo "[BOOT] $(date)" >> ascend_logs/boot_timestamps.log

# Init task queue
mkdir -p task_queue
echo "Launch full matrix." > task_queue/init.task

# Fire up loop engine and supervisor
python3 "Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py" &
python3 Ascend_Infra/Supervision/ascend_supervisor_agent.py &

echo ">> [Neo] Systems online. Awaiting LLaMA ignition."
