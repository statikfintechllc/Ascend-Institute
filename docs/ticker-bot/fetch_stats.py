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
        views_resp = requests.get(f"{base}/traffic/views", headers=HEADERS)
        clones_resp = requests.get(f"{base}/traffic/clones", headers=HEADERS)
        meta_resp = requests.get(base, headers=HEADERS)

        views = views_resp.json()
        clones = clones_resp.json()
        meta = meta_resp.json()

        if views_resp.status_code != 200 or clones_resp.status_code != 200:
            raise Exception(f"Views: {views_resp.status_code}, Clones: {clones_resp.status_code}")

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
