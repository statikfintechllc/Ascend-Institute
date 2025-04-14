# gpu_allocator.py

import ray
from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo

nvmlInit()

def get_available_gpus():
    gpu_count = nvmlDeviceGetCount()
    available_gpus = []
    for i in range(gpu_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        mem_info = nvmlDeviceGetMemoryInfo(handle)
        if mem_info.free > 1e9:  # Example threshold
            available_gpus.append(i)
    return available_gpus

@ray.remote(num_gpus=1)
def run_gpu_task(task_func, *args, **kwargs):
    return task_func(*args, **kwargs)