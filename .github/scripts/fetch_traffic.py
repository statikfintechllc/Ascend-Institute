import os
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
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
    plt.style.use('dark_background')
    timestamps = [datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M") for x in hist["traffic"]]
    views = [x['views'] for x in hist["traffic"]]
    clones = [x['clones'] for x in hist["traffic"]]

    # Calculate deltas for activity per interval
    views_delta = np.diff(views, prepend=views[0]) if len(views) > 0 else []
    clones_delta = np.diff(clones, prepend=clones[0]) if len(clones) > 0 else []

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, views_delta, color='#FFD700', marker='o', label='Views (interval)', linewidth=2)   # Gold
    ax.plot(timestamps, clones_delta, color='#FF3131', marker='o', label='Clones (interval)', linewidth=2) # Red

    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Count")
    ax.set_title("AscendAI GitHub Traffic (per 5 minutes)")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=30)
    ax.grid(True, color='#444444', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
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
