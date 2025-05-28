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

AGENT_PROFILE_PATH = os.path.abspath("agent_core/agent_profiles.yaml")

def load_agent_profiles():
    try:
        with open(AGENT_PROFILE_PATH, "r") as f:
            data = yaml.safe_load(f)
            agents = data.get("agents", {})
            profiles = data.get("profiles", {})
            return agents, profiles
    except Exception as e:
        logger.error(f"[AGENT_PROFILE] Failed to load profiles: {e}")
        return {}, {}

AGENTS, PROFILES = load_agent_profiles()

def resolve_agent_role(task_type):
    """
    Resolves which agent should handle a given task_type based on declared tool support.
    Returns the agent name, or 'default' if none match.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and task_type in profile["tools"]:
            logger.debug(f"[AGENT_PROFILE] Task type '{task_type}' assigned to agent '{agent_name}'")
            return agent_name
    logger.debug(f"[AGENT_PROFILE] Task type '{task_type}' assigned to default agent")
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

def all_agents():
    """
    Returns all agent names.
    """
    return list(AGENTS.keys())

def agent_supports_task(agent_name, task_type):
    """
    Returns True if the agent supports a given task_type.
    """
    profile = AGENTS.get(agent_name, {})
    return "tools" in profile and task_type in profile["tools"]
