# cloud_spawner.py

import subprocess
import logging

logger = logging.getLogger(__name__)

def apply_terraform(directory):
    subprocess.run(['terraform', 'init'], cwd=directory)
    subprocess.run(['terraform', 'apply', '-auto-approve'], cwd=directory)
    logger.info(f"Applied Terraform configuration in {directory}")