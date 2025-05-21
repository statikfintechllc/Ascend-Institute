#!/usr/bin/env python3

import os
import requests
import datetime
import matplotlib.pyplot as plt

OWNER = "statikfintechllc"
REPO = "AscendAI"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
CHART_PATH = "assets/traffic-chart.svg"

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

headers = {"Authorization": f"token {GITHUB_TOKEN}"}


def get_traffic(metric):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/{metric}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["clones" if metric == "clones" else "views"]


clones = get_traffic("clones")
views = get_traffic("views")

# Fall back to today with 0 values if GitHub returns empty traffic logs
if not clones or not views:
    today = datetime.datetime.utcnow()
    dates = [today]
    clone_counts = [0]
    view_counts = [0]
else:
    dates = [
        datetime.datetime.strptime(d["timestamp"][:10], "%Y-%m-%d") for d in clones
    ]
    clone_counts = [d["count"] for d in clones]
    view_counts = [d["count"] for d in views]

plt.figure(figsize=(6, 3))
plt.plot(dates, clone_counts, label="Clones", color="mediumvioletred")
plt.plot(dates, view_counts, label="Views", color="goldenrod")
plt.legend()
plt.title("AscendAI GitHub Traffic (last 14 days)")
plt.xlabel("Date")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(CHART_PATH, format="svg")
