How do we move them numbers lower??

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
    today = datetime.utcnow().date()
    return [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in reversed(range(n))
    ]


def plot_github_style_merged(
    clones, views, outfile,
    clones_today, unique_clones_today, views_today, unique_views_today,
    clones_14d, unique_clones_14d, views_14d, unique_views_14d,
    clones_lifetime, unique_clones_lifetime, views_lifetime, unique_views_lifetime
):
    plt.style.use('dark_background')
    last_14_days = get_last_n_days_iso(14)
    clones_dict = {item["timestamp"][:10]: item for item in clones}
    views_dict = {item["timestamp"][:10]: item for item in views}
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

    totals_str = (
        f"Today: Clones: {clones_today:,} | Unique Cloners: {unique_clones_today:,} | "
        f"Views: {views_today:,} | Unique Visitors: {unique_views_today:,}\n"
        f"14d: Clones: {clones_14d:,} | Unique Cloners: {unique_clones_14d:,} | "
        f"Views: {views_14d:,} | Unique Visitors: {unique_views_14d:,}\n"
        f"Lifetime: Clones: {clones_lifetime:,} | Unique Cloners: {unique_clones_lifetime:,} | "
        f"Views: {views_lifetime:,} | Unique Visitors: {unique_views_lifetime:,}"
    )
        fig.text(0.5, -0.08, totals_str, ha='center', va='bottom', color='#FFD700', fontsize=12, wrap=True)
    plt.tight_layout(rect=[0, 0.15, 1, 0.97])
    plt.savefig(outfile, bbox_inches='tight')
    plt.close()


def main(repo):
    clones_data = fetch("traffic/clones")
    views_data = fetch("traffic/views")

    with open("docs/traffic_data.json", "w") as f:
        json.dump({"clones": clones_data["clones"], "views": views_data["views"]}, f, indent=2)

    clones_lifetime = clones_data.get("count", 0)
    unique_clones_lifetime = clones_data.get("uniques", 0)
    views_lifetime = views_data.get("count", 0)
    unique_views_lifetime = views_data.get("uniques", 0)

    last_14_days = get_last_n_days_iso(14)
    clones_dict = {item["timestamp"][:10]: item for item in clones_data["clones"]}
    views_dict = {item["timestamp"][:10]: item for item in views_data["views"]}
    latest_day = last_14_days[-1]

    clones_today = clones_dict.get(latest_day, {}).get("count", 0)
    unique_clones_today = clones_dict.get(latest_day, {}).get("uniques", 0)
    views_today = views_dict.get(latest_day, {}).get("count", 0)
    unique_views_today = views_dict.get(latest_day, {}).get("uniques", 0)

    clones_14d = sum([item["count"] for item in clones_data["clones"]])
    unique_clones_14d = sum([item["uniques"] for item in clones_data["clones"]])
    views_14d = sum([item["count"] for item in views_data["views"]])
    unique_views_14d = sum([item["uniques"] for item in views_data["views"]])

    plot_github_style_merged(
        clones_data["clones"], views_data["views"], "docs/traffic_graph.png",
        clones_today, unique_clones_today, views_today, unique_views_today,
        clones_14d, unique_clones_14d, views_14d, unique_views_14d,
        clones_lifetime, unique_clones_lifetime, views_lifetime, unique_views_lifetime
    )

    with open("docs/traffic_totals.json", "w") as f:
        json.dump({
            "day": {
                "clones": clones_today,
                "uniqueClones": unique_clones_today,
                "views": views_today,
                "uniqueViews": unique_views_today
            },
            "range14d": {
                "clones": clones_14d,
                "uniqueClones": unique_clones_14d,
                "views": views_14d,
                "uniqueViews": unique_views_14d
            },
            "lifetime": {
                "clones": clones_lifetime,
                "uniqueClones": unique_clones_lifetime,
                "views": views_lifetime,
                "uniqueViews": unique_views_lifetime
            }
        }, f, indent=2)

    with open("docs/traffic_totals.md", "w") as f:
        f.write(f"""
**GitHub Traffic Totals**

- **Today:** Clones: {clones_today:,} | Unique Cloners: {unique_clones_today:,} | Views: {views_today:,} | Unique Visitors: {unique_views_today:,}
- **Last 14 days:** Clones: {clones_14d:,} | Unique Cloners: {unique_clones_14d:,} | Views: {views_14d:,} | Unique Visitors: {unique_views_14d:,}
- **Lifetime:** Clones: {clones_lifetime:,} | Unique Cloners: {unique_clones_lifetime:,} | Views: {views_lifetime:,} | Unique Visitors: {unique_views_lifetime:,}
""")


if __name__ == "__main__":
    main(REPO)
