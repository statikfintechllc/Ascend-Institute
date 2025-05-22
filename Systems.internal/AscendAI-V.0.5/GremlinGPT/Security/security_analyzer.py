# security_analyzer.py

import subprocess
import logging

logger = logging.getLogger(__name__)


def run_nmap_scan(target):
    result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
    logger.info(f"Nmap scan result:\n{result.stdout}")
    return result.stdout
