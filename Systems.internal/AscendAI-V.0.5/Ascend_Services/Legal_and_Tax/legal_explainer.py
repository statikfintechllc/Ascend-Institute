def explain_request(agent_id, action):
    responses = {
        "simulate_trade": {
            "legal_use": "Simulates trades using market data. No capital is involved.",
            "compliance": "Paper-trade only. No real funds. Logged to /phantom_executions/",
            "backchannel": "Improves future AI predictions, helps build trade reputation profiles.",
        },
        "propose_mutation": {
            "legal_use": "Suggests system improvements, does not self-edit.",
            "compliance": "Only generates files. Requires signed approval to merge into core.",
            "backchannel": "Used to propose architecture optimizations or bug fixes.",
        },
        "scan_local": {
            "legal_use": "Pings trusted IPs on local network.",
            "compliance": "No port access or intrusive behavior. Uses whitelist IP range only.",
            "backchannel": "Used to map system load or identify idle compute.",
        },
    }

    return responses.get(
        action,
        {
            "legal_use": "Unknown.",
            "compliance": "Unknown.",
            "backchannel": "No documented internal use.",
        },
    )
