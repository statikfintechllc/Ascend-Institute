import random

def mutate_dataset(dataset):
    mutated = []
    for entry in dataset:
        original = entry["log"]
        if "scrape" in original:
            fix = original.replace("fail", "retry")
        elif "scan" in original:
            fix = original.replace("low", "high")
        else:
            fix = original + " #mutated"

        mutated.append({
            "input": original,
            "mutation": fix,
            "label": "mutated"
        })
    return mutated

