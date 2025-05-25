import os
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
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
        json.dump(hist, f, indent=2)
    return hist

def plot_traffic(hist, outfile):
    timestamps = [x['timestamp'] for x in hist["traffic"]]
    views_list = [x['views'] for x in hist["traffic"]]
    clones_list = [x['clones'] for x in hist["traffic"]]

    # Calculate deltas for activity per interval
    views_deltas = np.diff(views_list, prepend=views_list[0]) if len(views_list) > 0 else []
    clones_deltas = np.diff(clones_list, prepend=clones_list[0]) if len(clones_list) > 0 else []

    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, views_deltas, label="Views")
    plt.plot(timestamps, clones_deltas, label="Clones")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.title("AscendAI GitHub Traffic (Interval Deltas)")
    plt.savefig(outfile)
    plt.close()

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
    hist = append_history("docs/traffic_data.json", "traffic", snapshot)
    plot_traffic(hist, "docs/traffic_graph.png")

if __name__ == "__main__":
    main(REPO)
