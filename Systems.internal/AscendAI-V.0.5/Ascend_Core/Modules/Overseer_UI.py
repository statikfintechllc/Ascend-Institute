import json
import os

REQUEST_DIR = "./dashboard/requests/"
RESPONSE_DIR = "./dashboard/responses/"


def load_requests():
    return [f for f in os.listdir(REQUEST_DIR) if f.endswith(".json")]


def display_request(req_id):
    with open(os.path.join(REQUEST_DIR, req_id), "r") as f:
        return json.load(f)


def save_response(req_id, decision):
    with open(os.path.join(RESPONSE_DIR, f"{req_id}_response.json"), "w") as f:
        json.dump({"request_id": req_id, "decision": decision}, f, indent=4)


# Example dashboard logic (text CLI, replace with UI layer as needed)
if __name__ == "__main__":
    for req in load_requests():
        data = display_request(req)
        print(
            f"\nAgent: {data['agent_id']}\nAction: {data['action']}\nContext: {data['context']}"
        )
        decision = input("Approve? (yes/no/details): ").strip().lower()
        if decision == "details":
            from legal_explainer import explain

            print(explain(data["action"]))
            decision = input("Final decision (yes/no): ").strip().lower()
        save_response(data["request_id"], decision)
