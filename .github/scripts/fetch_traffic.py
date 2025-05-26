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


def plot_github_style_merged(clones, views, outfile):
    plt.style.use('dark_background')

    # Parse data into dictionaries
    clones_dict = {item["timestamp"][:10]: item for item in clones}
    views_dict = {item["timestamp"][:10]: item for item in views}

    # Get overlapping dates in payload
    valid_dates = sorted(set(clones_dict.keys()) & set(views_dict.keys()))
    last_14_days = valid_dates[-14:]  # latest 14 shared dates
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in last_14_days]

    # Aligned values for plot
    clones_counts = [clones_dict[d]["count"] for d in last_14_days]
    unique_clones_counts = [clones_dict[d]["uniques"] for d in last_14_days]
    views_counts = [views_dict[d]["count"] for d in last_14_days]
    unique_views_counts = [views_dict[d]["uniques"] for d in last_14_days]

    # Most recent day (last available in data)
    latest_day = last_14_days[-1]
    clones_today = clones_dict[latest_day]["count"]
    unique_clones_today = clones_dict[latest_day]["uniques"]
    views_today = views_dict[latest_day]["count"]
    unique_views_today = views_dict[latest_day]["uniques"]

    # 14-day totals
    clones_14d = sum(clones_counts)
    unique_clones_14d = sum(unique_clones_counts)
    views_14d = sum(views_counts)
    unique_views_14d = sum(unique_views_counts)

    # Lifetime totals from payload
    clones_lifetime = sum(item["count"] for item in clones)
    unique_clones_lifetime = sum(item["uniques"] for item in clones)
    views_lifetime = sum(item["count"] for item in views)
    unique_views_lifetime = sum(item["uniques"] for item in views)

    # ─────────────── PLOT ───────────────
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
        f"Today ({latest_day}): Clones: {clones_today:,} | Unique Cloners: {unique_clones_today:,} | "
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

    return {
        "latest_day": latest_day,
        "clones_today": clones_today,
        "unique_clones_today": unique_clones_today,
        "views_today": views_today,
        "unique_views_today": unique_views_today,
        "clones_14d": clones_14d,
        "unique_clones_14d": unique_clones_14d,
        "views_14d": views_14d,
        "unique_views_14d": unique_views_14d,
        "clones_lifetime": clones_lifetime,
        "unique_clones_lifetime": unique_clones_lifetime,
        "views_lifetime": views_lifetime,
        "unique_views_lifetime": unique_views_lifetime
    }


def main(repo):
    clones_data = fetch("traffic/clones")
    views_data = fetch("traffic/views")

    os.makedirs("docs", exist_ok=True)

    with open("docs/traffic_data.json", "w") as f:
        json.dump({"clones": clones_data["clones"], "views": views_data["views"]}, f, indent=2)

    totals = plot_github_style_merged(
        clones_data["clones"], views_data["views"], "docs/traffic_graph.png"
    )

    with open("docs/traffic_totals.json", "w") as f:
        json.dump({
            "day": {
                "clones": totals["clones_today"],
                "uniqueClones": totals["unique_clones_today"],
                "views": totals["views_today"],
                "uniqueViews": totals["unique_views_today"]
            },
            "range14d": {
                "clones": totals["clones_14d"],
                "uniqueClones": totals["unique_clones_14d"],
                "views": totals["views_14d"],
                "uniqueViews": totals["unique_views_14d"]
            },
            "lifetime": {
                "clones": totals["clones_lifetime"],
                "uniqueClones": totals["unique_clones_lifetime"],
                "views": totals["views_lifetime"],
                "uniqueViews": totals["unique_views_lifetime"]
            }
        }, f, indent=2)

    with open("docs/traffic_totals.json", "w") as f:
        f.write(f"""
**GitHub Traffic Totals**

- **Today ({totals['latest_day']}):** Clones: {totals["clones_today"]:,} | Unique Cloners: {totals["unique_clones_today"]:,} | Views: {totals["views_today"]:,} | Unique Visitors: {totals["unique_views_today"]:,}
- **Last 14 days:** Clones: {totals["clones_14d"]:,} | Unique Cloners: {totals["unique_clones_14d"]:,} | Views: {totals["views_14d"]:,} | Unique Visitors: {totals["unique_views_14d"]:,}
- **Lifetime:** Clones: {totals["clones_lifetime"]:,} | Unique Cloners: {totals["unique_clones_lifetime"]:,} | Views: {totals["views_lifetime"]:,} | Unique Visitors: {totals["unique_views_lifetime"]:,}
""")
        # Inject totals into HTML widget
    with open("docs/dashboard.html", "r") as f:
        html = f.read()
        
    with open("docs/traffic_totals.json", "r") as f:
        totals = f.read()

    html = html.replace("{{TRAFFIC_TOTALS}}", totals.strip())

    with open("docs/dashboard.html", "w") as f:
        f.write(html)
    # Copy dashboard to index.html for GitHub Pages root
    with open("docs/dashboard.html", "r") as src:
        with open("docs/index.html", "w") as dst:
            dst.write(src.read())


if __name__ == "__main__":
    main(REPO)
