import requests, json, os

TOKEN = os.getenv("GH_TOKEN") or "ghp_xxx"  # Set in GitHub Secrets
HEADERS = {"Authorization": f"token {TOKEN}"}

repos = [
    "statikfintechllc/AscendAI", "statikfintechllc/Mobile-Developer",
    "statikfintechllc/AscendDocs-of-GovSeverance",
    "statikfintechllc/GodCore", "statikfintechllc/AscendNet"
]

stats = []
for repo in repos:
    views = requests.get(f"https://api.github.com/repos/{repo}/traffic/views", headers=HEADERS).json()
    clones = requests.get(f"https://api.github.com/repos/{repo}/traffic/clones", headers=HEADERS).json()

    stats.append({
        "repo": repo.split("/")[-1],
        "clones": clones.get("count", 0),
        "uniques": clones.get("uniques", 0),
        "views": views.get("count", 0),
        "visitors": views.get("uniques", 0)
    })

with open("docs/ticker-bot/stats.json", "w") as f:
    json.dump(stats, f)
