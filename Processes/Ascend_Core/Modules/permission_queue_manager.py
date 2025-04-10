import json
import uuid
from datetime import datetime

QUEUE_DIR = "./dashboard/requests/"

def queue_permission_request(agent_id, action, context=""):
    req_id = str(uuid.uuid4())
    request = {
        "request_id": req_id,
        "agent_id": agent_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat(),
        "context": context,
        "status": "pending"
    }

    with open(f"{QUEUE_DIR}/{req_id}.json", "w") as f:
        json.dump(request, f, indent=4)

    return req_id
