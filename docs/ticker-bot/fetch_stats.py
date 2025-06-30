# docs/ticker-bot/fetch_stats.py

import requests, json, os
from datetime import datetime

TOKEN = os.getenv("PAT_GITHUB")
HEADERS = {"Authorization": f"token {TOKEN}"}

REPOS = [
    "statikfintechllc/AscendAI",
    "statikfintechllc/Mobile-Developer",
    "statikfintechllc/AscendDocs-of-GovSeverance",
    "statikfintechllc/GodCore",
    "statikfintechllc/AscendNet"
]

stats = []

for repo in REPOS:
    owner, name = repo.split("/")
    base = f"https://api.github.com/repos/{owner}/{name}"

    try:
        views = requests.get(f"{base}/traffic/views", headers=HEADERS).json()
        clones = requests.get(f"{base}/traffic/clones", headers=HEADERS).json()
        meta = requests.get(base, headers=HEADERS).json()
        pulls = requests.get(f"{base}/pulls?state=open", headers=HEADERS).json()

        stats.append({
            "repo": name,
            "stars": meta.get("stargazers_count", 0),
            "forks": meta.get("forks_count", 0),
            "watchers": meta.get("subscribers_count", 0),
            "open_issues": meta.get("open_issues_count", 0),
            "language": meta.get("language", "N/A"),
            "size_kb": meta.get("size", 0),
            "default_branch": meta.get("default_branch", "main"),
            "updated_at": meta.get("updated_at", ""),
            "clones": clones.get("count", 0),
            "uniques": clones.get("uniques", 0),
            "views": views.get("count", 0),
            "visitors": views.get("uniques", 0),
            "pulls_count": len(pulls),
            "fetched": datetime.utcnow().isoformat()
        })

        print(f"[✔] {name} ✅ Views={views.get('count')} | Clones={clones.get('count')}")

    except Exception as e:
        print(f"[❌] Failed to fetch {repo}: {e}")

os.makedirs("docs/ticker-bot", exist_ok=True)
with open("docs/ticker-bot/stats.json", "w") as f:
    json.dump(stats, f, indent=2)
