import random
from datetime import datetime


def mutate_dataset(dataset):
    mutated = []
    for entry in dataset:
        original = entry["log"]
        mutation_type = None

        if "scrape" in original:
            fix = original.replace("fail", "retry")
            mutation_type = "scrape_retry"
        elif "scan" in original:
            fix = original.replace("low", "high")
            mutation_type = "signal_boost"
        else:
            suffixes = [
                " #mutated",
                f" #patch_{random.randint(100, 999)}",
                f" #delta_{datetime.utcnow().timestamp():.0f}",
            ]
            fix = original + random.choice(suffixes)
            mutation_type = "suffix_noise"

        mutated.append(
            {
                "input": original,
                "mutation": fix,
                "label": "mutated",
                "mutation_type": mutation_type,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    return mutated
