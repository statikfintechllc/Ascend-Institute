import json

ACL_FILE = "./config/agent_acl.json"


def load_acl():
    with open(ACL_FILE, "r") as f:
        return json.load(f)


def check_permission(agent_id, action):
    acl = load_acl()
    perms = acl.get(agent_id, {}).get("permissions", [])
    return action in perms


def log_and_notify(agent_id, action, result):
    out = {"agent_id": agent_id, "action": action, "result": result}
    with open(f"./dashboard/requests/{agent_id}_req.json", "w") as f:
        json.dump(out, f, indent=4)

    return result


def request_permission(agent_id, action):
    allowed = check_permission(agent_id, action)
    return log_and_notify(agent_id, action, "approved" if allowed else "denied")
