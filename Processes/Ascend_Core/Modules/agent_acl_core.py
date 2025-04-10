import json
import os

ACL_FILE = "./config/agent_acl.json"

def load_acl():
    if not os.path.exists(ACL_FILE):
        return {}

    with open(ACL_FILE, "r") as f:
        return json.load(f)

def has_permission(agent_id, action):
    acl = load_acl()
    perms = acl.get(agent_id, {}).get("permissions", [])
    return action in perms

def get_agent_roles(agent_id):
    acl = load_acl()
    return acl.get(agent_id, {}).get("roles", [])
