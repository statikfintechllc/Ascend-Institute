import json

class DashBridge:
    def __init__(self, queue_path="Dash_Sync/command_queue.json"):
        self.queue_path = queue_path

    def pull_commands(self):
        with open(self.queue_path, "r") as f:
            data = json.load(f)
        return data.get("commands", [])

    def push_command(self, cmd):
        with open(self.queue_path, "r") as f:
            data = json.load(f)
        data["commands"].append(cmd)
        with open(self.queue_path, "w") as f:
            json.dump(data, f, indent=4)

# Example usage:
# db = DashBridge()
# db.push_command("launch_godcore")
