# bridge_controller.py
import socket

ENV_PORTS = {
    "ai-core": 5101,
    "starcoder-wrapper": 5102,
    "nanogpt-wrapper": 5103,
    "ai-agents": 5104,
    "vector-db": 5105,
    "dashboard-ui": 5106,
    "quantum-research": 5107,
    "finops": 5108,
    "stealth-core": 5109,
    "surveillance-stack": 5110,
    "ml-ops-deploy": 5111,
    "netsec-tools": 5112,
    "telemetry-ops": 5113,
    "intel-recon": 5114,
    "darknet-interface": 5115,
    "ai-eval": 5116,
    "code-fuzz": 5117,
    "base-dev": 5118,
}


def send_to_env(env, python_code):
    port = ENV_PORTS[env]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", port))
        s.sendall(python_code.encode("utf-8"))
        response = s.recv(4096)
        return response.decode("utf-8")
