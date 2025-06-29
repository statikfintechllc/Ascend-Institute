import requests, json, os
from datetime import datetime

TOKEN = os.getenv("GH_TOKEN") or "ghp_xxx"
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

        stats.append({
            "repo": name,
            "stars": meta.get("stargazers_count", 0),
            "forks": meta.get("forks_count", 0),
            "clones": clones.get("count", 0),
            "uniques": clones.get("uniques", 0),
            "views": views.get("count", 0),
            "visitors": views.get("uniques", 0),
            "fetched": datetime.utcnow().isoformat()
        })
        print(f"[✔] {name} :: Views={views.get('count')} | Clones={clones.get('count')}")

    except Exception as e:
        print(f"[❌] Failed to fetch {repo}: {e}")

out_path = "docs/ticker-bot/stats.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as f:
    json.dump(stats, f, indent=2)
