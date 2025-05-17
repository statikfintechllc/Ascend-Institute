from collections import deque
import uuid

task_queue = deque()
task_status = {}

def enqueue_task(task):
    task_id = str(uuid.uuid4())
    task["id"] = task_id
    task_queue.append(task)
    task_status[task_id] = "queued"

def fetch_task(task_type=None):
    for _ in range(len(task_queue)):
        task = task_queue.popleft()
        if not task_type or task["type"] == task_type:
            task_status[task["id"]] = "running"
            return task
        task_queue.append(task)
    return None

def get_all_tasks():
    return [{"id": k, "status": v} for k, v in task_status.items()]

def update_task_status(task_id, status):
    task_status[task_id] = status

