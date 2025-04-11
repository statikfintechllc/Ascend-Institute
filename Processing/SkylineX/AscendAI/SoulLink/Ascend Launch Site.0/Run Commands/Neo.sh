#!/usr/bin/env python3

#run
chmod +x AS_SK_C4.py

#run
 ./AS_SK_C4.py

with open("ascend_logs/boot_timestamps.log", "a") as f:
    f.write(f"Booted at: {datetime.now()}\n")

with open("task_queue/init.task", "w") as f:
    f.write("Launch full matrix.\n")