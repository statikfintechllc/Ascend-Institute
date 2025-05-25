import os
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

REPO = os.environ.get("REPO")
TOKEN = os.environ.get("PAT_GITHUB")
HEADERS = {"Authorization": f"token {TOKEN}"}


def fetch(endpoint):
    url = f"https://api.github.com/repos/{REPO}/{endpoint}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_last_n_days_iso(n=14):
    # Returns list of ISO date strings for the last n days, oldest first
    today = datetime.utcnow().date()
    return [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in reversed(range(n))
    ]

def plot_github_style_merged(clones, views, outfile):
    plt.style.use('dark_background')

    # 1. Make sure we have a full list of the last 14 days (ISO date only)
    last_14_days = get_last_n_days_iso(14)

    # 2. Build dicts keyed by ISO date (YYYY-MM-DD)
    clones_dict = {item["timestamp"][:10]: item for item in clones}
    views_dict = {item["timestamp"][:10]: item for item in views}

    # 3. Build aligned lists for each day in last_14_days
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in last_14_days]
    clones_counts = [clones_dict.get(d, {}).get("count", 0) for d in last_14_days]
    unique_clones_counts = [clones_dict.get(d, {}).get("uniques", 0) for d in last_14_days]
    views_counts = [views_dict.get(d, {}).get("count", 0) for d in last_14_days]
    unique_views_counts = [views_dict.get(d, {}).get("uniques", 0) for d in last_14_days]

    fig, ax = plt.subplots(figsize=(12, 5))
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
    plt.savefig(outfile, bbox_inches='tight')
    plt.close()


def main(repo):
    clones_data = fetch("traffic/clones")
    views_data = fetch("traffic/views")

    # Save raw for JS/live chart if needed
    with open("docs/traffic_data.json", "w") as f:
        json.dump({"clones": clones_data["clones"], "views": views_data["views"]}, f, indent=2)

    # Plot merged graph
    plot_github_style_merged(clones_data["clones"], views_data["views"], "docs/traffic_graph.png")

    # Print current totals for display below the graph (optionally use in HTML)
    clones_total = sum([item["count"] for item in clones_data["clones"]])
    unique_clones_total = sum([item["uniques"] for item in clones_data["clones"]])
    views_total = sum([item["count"] for item in views_data["views"]])
    unique_views_total = sum([item["uniques"] for item in views_data["views"]])
    print(f"Clones (14d): {clones_total:,} | Unique Cloners (14d): {unique_clones_total:,}")
    print(f"Views (14d): {views_total:,} | Unique Visitors (14d): {unique_views_total:,}")


if __name__ == "__main__":
    main(REPO)
