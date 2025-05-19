# /agents/synthetic_identity_generator.py

import random
import json
from faker import Faker

faker = Faker()


def generate_identity():
    return {
        "name": faker.name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "location": faker.address(),
        "birthdate": faker.date_of_birth().isoformat(),
        "company": faker.company(),
        "role": random.choice(["CEO", "CTO", "Engineer", "Analyst"]),
        "avatar_seed": random.randint(1000, 9999),
    }


if __name__ == "__main__":
    identity = generate_identity()
    print(json.dumps(identity, indent=4))
