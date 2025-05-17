# api_mutator.py

import httpx
import random
import string

def mutate_payload(payload):
    mutated = payload.copy()
    for key in mutated:
        mutated[key] = ''.join(random.choices(string.ascii_letters, k=10))
    return mutated

def send_mutated_request(url, original_payload):
    mutated = mutate_payload(original_payload)
    response = httpx.post(url, json=mutated)
    return response