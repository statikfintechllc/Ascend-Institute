import os, requests, json
import matplotlib.pyplot as plt
from datetime import datetime

REPO = os.environ.get("REPO")
TOKEN = os.environ.get("PAT_GITHUB")
HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch(endpoint):
    url = f"https://api.github.com/repos/{REPO}/{endpoint}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def append_history(datafile, key, new_data):
    try:
        with open(datafile, 'r') as f:
            hist = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        hist = {key: []}
    hist.setdefault(key, []).append(new_data)
    with open(datafile, 'w') as f:
        json.dump(hist, f)
    return hist

def main(repo):
    clones = fetch("traffic/clones")
    views = fetch("traffic/views")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    snapshot = {
        "timestamp": now,
        "clones": clones.get("count", 0),
        "uniques_clones": clones.get("uniques", 0),
        "views": views.get("count", 0),
        "uniques_views": views.get("uniques", 0)
    }
    hist = append_history("traffic_data.json", "traffic", snapshot)

    # Generate graph
    timestamps = [x['timestamp'] for x in hist["traffic"]]
    views = [x['views'] for x in hist["traffic"]]
    clones = [x['clones'] for x in hist["traffic"]]

    plt.figure(figsize=(10,4))
    plt.plot(timestamps, views, label="Views")
    plt.plot(timestamps, clones, label="Clones")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.title("AscendAI GitHub Traffic Over Time")
    plt.savefig("traffic_graph.png")
    plt.close()

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
