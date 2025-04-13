
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def detect_xbox():
    print("[] Scanning for Xbox on network...")
    xbox_ip = None
    # Scan local network for Xbox (using broadcast UDP packets)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
        for i in range(1, 255):
            target_ip = f"192.168.1.{i}"
            sock.sendto(b'XBOX_DISCOVERY', (target_ip, 5050))
            response, addr = sock.recvfrom(1024)
            if b'XBOX' in response:
                xbox_ip = addr[0]
                break
    except socket.timeout:
    sock.close()
    return xbox_ip

if __name__ == '__main__':
    detect_xbox()