#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: agent_core/agent_profile.py

import yaml
import os
from backend.globals import logger

AGENT_PROFILE_PATH = os.path.abspath(
    os.environ.get("AGENT_PROFILE_PATH", "agent_core/agent_profiles.yaml")
)


def load_agent_profiles():
    try:
        with open(AGENT_PROFILE_PATH, "r") as f:
            data = yaml.safe_load(f)
            agents = data.get("agents", {})
            profiles = data.get("profiles", {})
            # Validate that each agent's 'tools' field is a list or set, or set to empty list if missing/invalid
            for agent_name, profile in agents.items():
                tools = profile.get("tools", [])
                if not isinstance(tools, (list, set)):
                    logger.warning(f"[AGENT_PROFILE] Agent '{agent_name}' has invalid 'tools' field. Setting to empty list.")
                    profile["tools"] = []
            return agents, profiles
    except Exception as e:
        logger.error(f"[AGENT_PROFILE] Failed to load profiles: {e}")
        return {}, {}
AGENTS, PROFILES = load_agent_profiles()

def reload_agent_profiles():
    """
    Reloads agent and profile data from the YAML file and updates globals.
    """
    global AGENTS, PROFILES
    AGENTS, PROFILES = load_agent_profiles()
    logger.info("[AGENT_PROFILE] Agent profiles reloaded from YAML file.")

AGENTS, PROFILES = load_agent_profiles()


def resolve_agent_role(task_type):
    """
    Resolves which agent should handle a given task_type based on declared tool support.
    Returns the agent name, or 'default' if none match.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and task_type in profile["tools"]:
            return agent_name
    return "default"


def get_agent_profile(agent_name):
    """
    Returns the full agent profile for a given agent name.
    """
    return AGENTS.get(agent_name, AGENTS.get("default", {}))


def get_profile_details(profile_name):
    """
    Returns the extended profile (role/capabilities/isolation/priority) for a profile name.
    """
    return PROFILES.get(profile_name, {})


def agent_supports_task(agent_name, task_type):
    """
    Returns True if the agent supports a given task_type.
    """
    profile = AGENTS.get(agent_name, {})
    return "tools" in profile and task_type in profile["tools"]
