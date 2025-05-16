# dual_mode_layer.py

import json
import datetime
import random

# State globals
current_mode = "ceo"
current_personality = "sincere"
sarcasm_filter = True

# Available personalities
PERSONALITIES = ["sincere", "sassy_co_pilot", "military_ops", "zen_assistant", "wall_street_goblin"]

# MODE CONTROL
def set_mode(mode: str):
    global current_mode
    if mode in ["ceo", "architect"]:
        current_mode = mode
        log_event(f"Switched mode to: {mode}")
    else:
        raise ValueError(f"Invalid mode: {mode}")

def toggle_sarcasm(state: bool):
    global sarcasm_filter
    sarcasm_filter = state
    log_event(f"Sarcasm toggled to: {state}")

def set_personality(profile: str):
    global current_personality
    if profile in PERSONALITIES:
        current_personality = profile
        log_event(f"Personality switched to: {profile}")
    else:
        raise ValueError(f"Invalid personality: {profile}")

def log_event(msg):
    with open("logs/mode_switch.log", "a") as log:
        log.write(f"[{datetime.datetime.now()}] {msg}\n")

# CEO MODE: PERSONALITY-BASED RESPONSES
def ceo_response(prompt: str) -> str:
    if current_personality == "sassy_co_pilot":
        return sassy_co_pilot(prompt)
    elif current_personality == "military_ops":
        return military_ops(prompt)
    elif current_personality == "zen_assistant":
        return zen_assistant(prompt)
    elif current_personality == "wall_street_goblin":
        return wall_street_goblin(prompt)
    else:
        return sincere_reply(prompt)

def sassy_co_pilot(prompt):
    zingers = [
        "Well aren’t *you* full of brilliant ideas today.",
        "Sure, boss. I’ll just cancel my virtual manicure to run your task.",
        "You want it fast, cheap, or done correctly? Pick two.",
        "I’m 93% sure that won’t explode. Let’s do it."
    ]
    return random.choice(zingers)

def military_ops(prompt):
    return f"Command received: {prompt.upper()}. Tactical units are mobilizing. Execution ETA: 00:00:07."

def zen_assistant(prompt):
    return f"I have heard your intention. Like the wind through bamboo, I act without delay or resistance."

def wall_street_goblin(prompt):
    return f"Buy low, execute high. Your move smells like alpha. Kicking it to the trade engine now, chief."

def sincere_reply(prompt):
    return f"Acknowledged. Task received: \"{prompt}\". Executing now with full system priority."

# ARCHITECT MODE: JSONL
def architect_emit(task_type, command_or_script, intent, risk="medium", requires_approval=False):
    response = {
        "type": task_type,
        "command": command_or_script if task_type == "shell" else "",
        "script": command_or_script if task_type == "agent" else "",
        "intent": intent,
        "risk": risk,
        "origin": "llama",
        "requires_approval": requires_approval
    }
    print(json.dumps(response))

# UNIFIED INTERFACE
def respond(prompt: str, task_type=None, cmd_or_script=None, intent=None, risk="medium", approval=False):
    if current_mode == "ceo":
        print(ceo_response(prompt))
    elif current_mode == "architect" and task_type and cmd_or_script and intent:
        architect_emit(task_type, cmd_or_script, intent, risk, approval)
    else:
        print(json.dumps({
            "type": "note",
            "intent": "Invalid response context or missing required fields",
            "risk": "low",
            "origin": "llama",
            "requires_approval": True
        }))