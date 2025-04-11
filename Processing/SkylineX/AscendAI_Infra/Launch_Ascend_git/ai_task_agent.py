
import time
import requests

class AIAgent:
    def __init__(self):
        self.base_url = "http://localhost:5000"  # Assuming the AI core runs on this endpoint

    def monitor_system(self):
        print("Monitoring system status...")
        try:
            response = requests.get(f"{self.base_url}/status")
            print("System Status:", response.json())
        except Exception as e:
            print("Error during system monitoring:", e)

    def perform_decision_making(self):
        print("Performing decision-making tasks...")
        try:
            response = requests.post(f"{self.base_url}/decision", json={"task": "optimize_resources"})
            print("Decision Response:", response.json())
        except Exception as e:
            print("Error during decision-making:", e)

    def detect_errors(self):
        print("Checking for system errors...")
        try:
            response = requests.get(f"{self.base_url}/errors")
            if response.json().get("errors"):
                print("Errors detected:", response.json())
            else:
                print("No errors detected.")
        except Exception as e:
            print("Error during error detection:", e)

if __name__ == "__main__":
    agent = AIAgent()
    while True:
        agent.monitor_system()
        agent.perform_decision_making()
        agent.detect_errors()
        time.sleep(10)
