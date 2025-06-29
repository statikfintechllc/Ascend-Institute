import requests, json, os

TOKEN = os.getenv("GH_TOKEN") or "ghp_xxx"  # Secure token in GitHub secrets
HEADERS = {"Authorization": f"token {TOKEN}"}

repos = [
    "statikfintechllc/AscendAI",
    "statikfintechllc/Mobile-Developer",
    "statikfintechllc/AscendDocs-of-GovSeverance",
    "statikfintechllc/GodCore",
    "statikfintechllc/AscendNet"
]

stats = []

for repo in repos:
    owner, name = repo.split("/")
    base = f"https://api.github.com/repos/{owner}/{name}"

    views = requests.get(f"{base}/traffic/views", headers=HEADERS).json()
    clones = requests.get(f"{base}/traffic/clones", headers=HEADERS).json()
    meta   = requests.get(base, headers=HEADERS).json()

    stats.append({
        "repo": name,
        "stars": meta.get("stargazers_count", 0),
        "forks": meta.get("forks_count", 0),
        "clones": clones.get("count", 0),
        "uniques": clones.get("uniques", 0),
        "views": views.get("count", 0),
        "visitors": views.get("uniques", 0)
    })

with open("docs/ticker-bot/stats.json", "w") as f:
    json.dump(stats, f, indent=2)
