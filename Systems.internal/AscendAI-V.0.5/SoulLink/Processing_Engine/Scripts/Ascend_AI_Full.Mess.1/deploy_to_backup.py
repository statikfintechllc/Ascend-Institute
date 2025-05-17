
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def deploy_to_backup():
    print(" Deploying AI Across Multiple Systems...")
    for node in backup_nodes:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(node, username=os.getenv('SSH_USER'), password=os.getenv('SSH_PASS'))
            sftp = ssh.open_sftp()
            sftp.put(sys.argv[0], "/root/Ascend_AI.py")
            sftp.close()
            ssh.exec_command("python3 /root/Ascend_AI.py &")
            ssh.close()
            print(f" Successfully deployed Ascend to {node}")
        except Exception as e:
            print(f" Failed to deploy to {node}: {e}")

if __name__ == '__main__':
    deploy_to_backup()