import os
import requests
import json
import matplotlib.pyplot as plt
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

def plot_github_style_merged(clones, views, outfile):
    plt.style.use('dark_background')

    # Extract daily stats
    dates = [datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%SZ") for item in clones]
    clones_counts = [item["count"] for item in clones]
    unique_clones_counts = [item["uniques"] for item in clones]
    views_counts = [item["count"] for item in views]
    unique_views_counts = [item["uniques"] for item in views]

    fig, ax = plt.subplots(figsize=(12, 5))

    # Plot all four series
    ax.plot(dates, clones_counts, color='#FF3131', marker='o', label='Clones', linewidth=2)
    ax.plot(dates, unique_clones_counts, color='#46D160', marker='o', label='Unique Cloners', linewidth=2)
    ax.plot(dates, views_counts, color='#FFD700', marker='o', label='Views', linewidth=2)
    ax.plot(dates, unique_views_counts, color='#2188ff', marker='o', label='Unique Visitors', linewidth=2)

    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.set_title("AscendAI GitHub Traffic (Last 14 Days)")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xticks(rotation=30)
    ax.grid(True, color='#444444', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.savefig(outfile, bbox_inches='2')
    plt.close()

def main(repo):
    clones_data = fetch("traffic/clones")
    views_data = fetch("traffic/views")

    # Save raw for JS/live chart if needed
    with open("docs/traffic_data.json", "w") as f:
        json.dump({"clones": clones_data["clones"], "views": views_data["views"]}, f, indent=2)

    # Plot merged graph
    plot_github_style_merged(clones_data["clones"], views_data["views"], "docs/traffic_graph.png")

if __name__ == "__main__":
    main(REPO)
