import os
import re
import json
import time
import subprocess

# Predefined critical files with AI logic templates that evolve over time
CRITICAL_FILES = {
    "preprocess.py": (
        "/data_pipeline/preprocess.py",
        """import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)

    le = LabelEncoder()
    if 'label' in df.columns:
        df['label'] = le.fit_transform(df['label'])

    scaler = StandardScaler()
    X = scaler.fit_transform(df.drop('label', axis=1))
    y = df['label'].values

    return X, y""",
    ),
    "model.py": (
        "/models/model.py",
        """import torch.nn as nn

class EvolvingNN(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_size=128):
        super(EvolvingNN, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_dim)
        )
    def forward(self, x):
        return self.layers(x)""",
    ),
    "train.py": (
        "/training/train.py",
        """import torch
import torch.nn as nn
import torch.optim as optim
from model import EvolvingNN

def train_model(X_train, y_train, epochs=10, lr=0.001, hidden_size=128):
    model = EvolvingNN(X_train.shape[1], len(set(y_train)), hidden_size)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

    return model""",
    ),
    "watchdog.py": (
        "/monitoring/watchdog.py",
        """import subprocess, time

def monitor(script="train.py"):
    while True:
        print(f"Running {script}")
        p = subprocess.Popen(["python", script])
        p.wait()
        print(f"{script} exited. Restarting in 5s...")
        time.sleep(5)

if __name__ == "__main__":
    monitor()""",
    ),
    "memory_engine.py": (
        "/core/memory_engine.py",
        """import faiss, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)

def store_embedding(text):
    vec = model.encode([text])
    index.add(vec)

def search_embedding(query):
    vec = model.encode([query])
    _, I = index.search(vec, k=1)
    return I""",
    ),
}


def scan_and_self_optimize(directory="Ascend_AI"):
    iteration = 0
    while iteration < 10:  # Self-learning loop for 10 iterations
        print(f"--- [Self-Optimization Iteration {iteration}] ---")
        scanned_files = {}
        missing_files = []

        # Scan and track files
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                scanned_files[file] = full_path

        # Identify and upgrade missing AI modules
        for required_file, (path, content) in CRITICAL_FILES.items():
            target_path = os.path.join(directory, path)
            if required_file not in scanned_files or needs_upgrade(
                target_path
            ):
                missing_files.append(
                    {
                        "file": required_file,
                        "path": target_path,
                        "content": content,
                    }
                )

        # Rebuild missing or outdated AI components
        for missing in missing_files:
            os.makedirs(os.path.dirname(missing["path"]), exist_ok=True)
            with open(missing["path"], "w", encoding="utf-8") as f:
                f.write(missing["content"])
            print(
                f"Upgraded AI module: {missing['file']} at {missing['path']}"
            )

        # Run AI self-tests and evolve
        run_all_tests()
        evolve_logic()
        iteration += 1
        time.sleep(5)  # Small delay before next iteration


def needs_upgrade(file_path):
    """Check if the file needs an upgrade based on versioning or size growth"""
    return (
        os.path.getsize(file_path) < 1024
    )  # If file is too small, consider upgrading


def run_all_tests():
    """Run all AI system tests dynamically"""
    print("[TEST] Running AI system tests...")
    try:
        subprocess.run(["pytest", "--disable-warnings"], check=True)
        print("[TEST] All tests passed.")
    except subprocess.CalledProcessError:
        print("[TEST] Some tests failed. AI will attempt fixes.")


def evolve_logic():
    """AI self-improvement logic: adjusts model complexity and retrains"""
    print("[EVOLVE] Enhancing AI logic dynamically...")
    model_file = os.path.join("Ascend_AI", "models", "model.py")

    # Example: Increase hidden layers dynamically
    with open(model_file, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "hidden_size=" in line:
                num = int(re.findall(r"\d+", line)[0])
                new_size = num + 32
                lines[i] = f"        self.hidden_size = {new_size}\n"
                print(f"[EVOLVE] Increasing hidden layer size: {new_size}")
        f.seek(0)
        f.writelines(lines)
        f.truncate()


if __name__ == "__main__":
    scan_and_self_optimize()
