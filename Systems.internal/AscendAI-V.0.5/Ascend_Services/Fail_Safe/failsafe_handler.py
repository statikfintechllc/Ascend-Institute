import json
import time

class FailSafe:
    def __init__(self, config_path="Fail_Safe/system_failsafe.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def trigger(self, condition):
        if condition in self.config.get("trigger_conditions", []):
            print(f"[FAILSAFE] Condition triggered: {condition}")
            if self.config.get("log_on_trigger"):
                self.log(condition)
            if self.config.get("auto_reboot"):
                self.reboot()
            if self.config.get("notify_ceo"):
                self.notify_ceo()
        else:
            print(f"[FAILSAFE] Condition ignored: {condition}")

    def log(self, condition):
        with open("Fail_Safe/failsafe_log.txt", "a") as log:
            log.write(f"[{time.ctime()}] FAILSAFE TRIGGERED: {condition}
")

    def reboot(self):
        print("[FAILSAFE] Rebooting fallback module...")
        # Simulated reboot: in production, this would re-execute main logic
        exec(open(self.config["fallback_module"]).read())

    def notify_ceo(self):
        print(f"[FAILSAFE] Notifying CEO at {self.config['ceo_contact']} (simulated)")
