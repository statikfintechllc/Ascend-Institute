import os


def extract_training_data(log_dir):
    entries = []
    for file in os.listdir(log_dir):
        if file.endswith(".log"):
            with open(os.path.join(log_dir, file), "r") as f:
                lines = f.readlines()
            for line in lines:
                if any(bad in line for bad in ["FAIL", "LOW_CONF", "INVALID"]):
                    entries.append({"log": line.strip()})
    return entries
