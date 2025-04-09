#!/bin/bash

chmod +x AS_SK_C4.py
./AS_SK_C4.py

echo "[BOOT] $(date)" >> ascend_boot.log
echo "Launch full matrix." >> task_queue/init.task

python3 "Private.internal/Ascend_Infra/Launch_Ascend/loop_engine.py" &

from datetime import datetime
with open("ascend_logs/boot_timestamps.log", "a") as f:
    f.write(f"Booted at: {datetime.now()}\n")

with open("task_queue/init.task", "w") as f:
    f.write("Launch full matrix.\n")
