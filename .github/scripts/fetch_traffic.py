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
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    plt.style.use('dark_background')
    timestamps = [datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M") for x in hist["traffic"]]
    views = [x['views'] for x in hist["traffic"]]
    clones = [x['clones'] for x in hist["traffic"]]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, views, color='#FFD700', marker='o', label='Views (14-day rolling total)', linewidth=2)
    ax.plot(timestamps, clones, color='#FF3131', marker='o', label='Clones (14-day rolling total)', linewidth=2)

    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("14-day Total")
    ax.set_title("AscendAI GitHub Traffic (14-day rolling totals)")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=30)
    ax.grid(True, color='#444444', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.savefig(outfile, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main(REPO)
