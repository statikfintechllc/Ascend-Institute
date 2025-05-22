import json
import time


def ping_dashboard():
    with open("Dash_Sync/sync_status.json", "r") as f:
        status = json.load(f)
    status["last_sync"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open("Dash_Sync/sync_status.json", "w") as f:
        json.dump(status, f, indent=4)
    print("[Ascend] Dashboard pinged.")


if __name__ == "__main__":
    ping_dashboard()
