
import os
import subprocess
import datetime

REPO_DIR = "."  # Root of Ascend-AI project

def git_init():
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        subprocess.run(["git", "init"], cwd=REPO_DIR)
        subprocess.run(["git", "config", "user.name", "AscendAI"], cwd=REPO_DIR)
        subprocess.run(["git", "config", "user.email", "ai@ascend.local"], cwd=REPO_DIR)
        print("✅ Initialized local Git repository")

def git_commit_all(message="AI system update"):
    timestamp = datetime.datetime.now().isoformat()
    subprocess.run(["git", "add", "."], cwd=REPO_DIR)
    subprocess.run(["git", "commit", "-m", f"{message} | {timestamp}"], cwd=REPO_DIR)
    print(f"✅ Committed all changes: {message}")

def git_branch_experiment(branch_name="ascend-exp"):
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=REPO_DIR)
    print(f"🌱 Created experimental branch: {branch_name}")

def git_push(remote_url):
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=REPO_DIR)
    subprocess.run(["git", "branch", "-M", "main"], cwd=REPO_DIR)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=REPO_DIR)

if __name__ == "__main__":
    git_init()
    git_commit_all("Initial sync of Ascend-AI system")
